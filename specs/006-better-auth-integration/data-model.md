# Data Model: Better Auth Integration

## Database Schema

### Users Table
- **id** (text, primary key): Unique identifier for the user
- **email** (text, not null, unique): User's email address
- **emailVerified** (timestamp): Timestamp when email was verified
- **name** (text): User's display name
- **createdAt** (timestamp, not null): Account creation timestamp
- **updatedAt** (timestamp, not null): Last update timestamp

### Sessions Table
- **id** (text, primary key): Unique session identifier
- **userId** (text, not null, foreign key): Reference to users table
- **expiresAt** (timestamp, not null): Session expiration timestamp
- **token** (text, not null): Session token value
- **createdAt** (timestamp, not null): Session creation timestamp
- **updatedAt** (timestamp, not null): Last update timestamp

### JWKS Table
- **id** (text, primary key): Unique identifier for the key pair
- **publicKey** (text, not null): Public key in JSON format for JWT verification
- **privateKey** (text, not null): Private key for JWT signing (encrypted)
- **createdAt** (timestamp, not null): Key creation timestamp

## Entity Relationships
- Users to Sessions: One-to-many (one user can have multiple active sessions)
- No direct relationship between Users and JWKS (JWKS contains public/private key pairs used system-wide)

## Validation Rules
- Email must be unique across all users
- Email must follow standard email format
- Session expiration must be in the future
- User ID in sessions must reference an existing user
- CreatedAt and UpdatedAt fields are automatically managed

## State Transitions
- User registration: Creates user record with unverified email
- Email verification: Updates emailVerified timestamp
- Login: Creates new session record
- Logout: Invalidates session by deleting session record
- Session expiration: Session becomes invalid after expiresAt timestamp