// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.19.1

package sqlite

import (
	"database/sql"
)

type Event struct {
	ID           sql.NullInt64
	Name         string
	Description  sql.NullString
	Issuer       sql.NullInt64
	StartingAt   sql.NullTime
	EndingAt     sql.NullTime
	MaxAmount    sql.NullInt64
	MaxPerPerson sql.NullInt64
}

type Offer struct {
	ID     sql.NullInt64
	Issuer sql.NullInt64
	Amount int64
}

type Tab struct {
	ID     sql.NullInt64
	UserID sql.NullInt64
	Amount int64
	At     sql.NullTime
}

type User struct {
	ID       sql.NullInt64
	Username sql.NullString
	Email    string
	Credit   sql.NullInt64
}