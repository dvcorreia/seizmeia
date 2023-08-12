package auth

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	"fmt"
	"net/http"
	"net/url"

	"github.com/coreos/go-oidc/v3/oidc"
	"golang.org/x/oauth2"
)

type Option func(*authenticator) error

type Options struct {
	// OAuth2 client ID of this application.
	ClientID string

	// OAuth2 client secret of this application.
	ClientSecret string

	// URL of the OpenID Connect issuer.
	IssuerURL string

	// Callback URL for OAuth2 responses.
	RedirectURI string
}

func WithOptions(opts Options) Option {
	return func(a *authenticator) error {
		if opts.ClientID != "" {
			a.clientID = opts.ClientID
		}

		if opts.ClientSecret != "" {
			a.clientSecret = opts.ClientSecret
		}

		if opts.IssuerURL != "" {
			u, err := url.Parse(opts.IssuerURL)
			if err != nil {
				return fmt.Errorf("issue url: %w", err)
			}

			a.issuerURL = *u
		}

		if opts.RedirectURI != "" {
			u, err := url.Parse(opts.RedirectURI)
			if err != nil {
				return fmt.Errorf("redirect uri: %w", err)
			}

			a.redirectURI = *u
		}

		return nil
	}
}

type authenticator struct {
	clientID     string
	clientSecret string
	redirectURI  url.URL

	verifier *oidc.IDTokenVerifier
	provider *oidc.Provider

	issuerURL url.URL

	// Does the provider use "offline_access" scope to request a refresh token
	// or does it use "access_type=offline" (e.g. Google)?
	offlineAsScope bool

	client *http.Client

	SpaRedirectURI url.URL
}

func New(options ...Option) (*authenticator, error) {
	a := &authenticator{
		client: http.DefaultClient,
	}

	for _, opt := range options {
		if err := opt(a); err != nil {
			return nil, err
		}
	}

	ctx := oidc.ClientContext(context.Background(), a.client)
	provider, err := oidc.NewProvider(ctx, a.issuerURL.String())
	if err != nil {
		return nil, fmt.Errorf("creating oidc provider: %w", err)
	}

	var s struct {
		// What scopes does a provider support?
		//
		// See: https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata
		ScopesSupported []string `json:"scopes_supported"`
	}
	if err := provider.Claims(&s); err != nil {
		return nil, fmt.Errorf("failed to parse provider scopes_supported: %v", err)
	}

	if len(s.ScopesSupported) == 0 {
		// scopes_supported is a "RECOMMENDED" discovery claim, not a required
		// one. If missing, assume that the provider follows the spec and has
		// an "offline_access" scope.
		a.offlineAsScope = true
	} else {
		// See if scopes_supported has the "offline_access" scope.
		a.offlineAsScope = func() bool {
			for _, scope := range s.ScopesSupported {
				if scope == oidc.ScopeOfflineAccess {
					return true
				}
			}
			return false
		}()
	}

	a.provider = provider
	a.verifier = provider.Verifier(&oidc.Config{ClientID: a.clientID})

	return a, nil
}

func (a *authenticator) oauth2Config(scopes []string) *oauth2.Config {
	return &oauth2.Config{
		ClientID:     a.clientID,
		ClientSecret: a.clientSecret,
		Endpoint:     a.provider.Endpoint(),
		Scopes:       scopes,
		RedirectURL:  a.redirectURI.String(),
	}
}

func (a *authenticator) newState() string {
	buf := make([]byte, 1024)
	rand.Read(buf)

	h := sha256.New()
	h.Write(buf)

	return fmt.Sprintf("%x", h.Sum(nil))
}
