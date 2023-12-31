NAME ?= seizmeia
DESCRIPTION ?= A credit management tool for a beer tap.

VERSION ?= $(shell git describe --tags --exact-match 2>/dev/null || git symbolic-ref -q --short HEAD)
COMMIT_HASH ?= $(shell git rev-parse --short HEAD 2>/dev/null)
COMMIT_HASH_LONG ?= $(shell git rev-parse HEAD 2>/dev/null)

REMOTE ?= $(shell git ls-remote --get-url 2>/dev/null)
GIT_SERVICE ?= $(shell echo "$(REMOTE)" | cut -d ":" -f1 | cut -d "@" -f2)
SOURCE ?= https://$(GIT_SERVICE)/$(shell echo $(REMOTE) | cut -d ":" -f2)
URL ?= $(shell echo "$(SOURCE)" | rev | cut -c 5- | rev)
MAIN_BRANCH ?= $(shell git symbolic-ref refs/remotes/origin/HEAD | cut -d "/" -f4)

DATE_FMT = +%FT%TZ # ISO 8601
BUILD_DATE ?= $(shell date "$(DATE_FMT)") # "-u" for UTC time (zero offset)

BUILD_DIR ?= build
LDFLAGS += -X main.version=$(VERSION) -X main.commitHash=$(COMMIT_HASH) -X main.buildDate=$(BUILD_DATE)

.DEFAULT_GOAL: help
default: help

.PHONY: run-%
run-%: build-% 
	$(BUILD_DIR)/$*

.PHONY: build-%
build-%:
	@mkdir -p $(BUILD_DIR)
	go build $(GOARGS) -ldflags "$(LDFLAGS)" -o $(BUILD_DIR)/$* ./cmd/$*

.PHONY: test coverage
test:
	CGO_ENABLED=1 go test -v -race -cover $(TEST_PKGS)
coverage:
	@CGO_ENABLED=1 go test -ldflags "${LDFLAGS}" -short $(TEST_PKGS) -coverprofile cover.out 2>/dev/null
	@go tool cover -func cover.out

.PHONY: lint
lint: ## lint code
	@golangci-lint run ./...
lint-podman:
	podman build --target lint -f tools/Dockerfile --tag $(NAME):$(VERSION)-lint .
	podman run $(NAME):$(VERSION)-lint

##@ Clean
clean: ## Delete all builds and downloaded dependencies.
	@rm -rf bin/

FORMATTING_BEGIN_YELLOW = \033[0;33m
FORMATTING_BEGIN_BLUE = \033[36m
FORMATTING_END = \033[0m

.PHONY: help
help:
	@printf -- "${FORMATTING_BEGIN_BLUE}%s${FORMATTING_END}\n" \
	"" \
	"  .~~~~.                                                      " \
	"  i====i_                                                     " \
	"  |cccc|_)                                                    " \
	"  |cccc|   Seizmeia: A credit management tool for a beer tap  " \
	"  \`-==-'                                                     " \
	"" \
	"--------------------------------------------------------------" \
	""
	@awk 'BEGIN {\
	    FS = ":.*##"; \
	    printf                "Usage: ${FORMATTING_BEGIN_BLUE}OPTION${FORMATTING_END}=<value> make ${FORMATTING_BEGIN_YELLOW}<target>${FORMATTING_END}\n"\
	  } \
	  /^[a-zA-Z0-9_-]+:.*?##/ { printf "  ${FORMATTING_BEGIN_BLUE}%-46s${FORMATTING_END} %s\n", $$1, $$2 } \
	  /^.?.?##~/              { printf "   %-46s${FORMATTING_BEGIN_YELLOW}%-46s${FORMATTING_END}\n", "", substr($$1, 6) } \
	  /^##@/                  { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)