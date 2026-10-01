# Mermaid Diagram Patterns

Ready-to-use syntax patterns for UX flow diagrams.

## Table of Contents

- [Flowchart Patterns](#flowchart-patterns)
- [State Diagram Patterns](#state-diagram-patterns)
- [Sequence Diagram Patterns](#sequence-diagram-patterns)
- [Best Practices](#best-practices)

---

## Flowchart Patterns

### Node Shapes

Use consistent shapes across all flowcharts:

```
[Screen Name]       — Rectangle: screens/pages
{Decision?}         — Diamond: conditional branch
((Start))           — Circle: entry point
([Action])          — Stadium: user action
[[Sub-flow]]        — Subroutine: link to another diagram
>Result]            — Asymmetric: outcome/redirect
```

### Subgraphs for Screen Groups

Group related screens:

```mermaid
graph TD
    subgraph Auth["Authentication"]
        Login[Login Screen]
        Register[Register Screen]
        ForgotPW[Forgot Password]
    end

    subgraph Main["Main App"]
        Home[Home Screen]
        Profile[Profile Screen]
        Settings[Settings Screen]
    end

    Login -->|Success| Home
    Login -->|New User| Register
    Login -->|Forgot| ForgotPW
    Register -->|Complete| Home
    Home --> Profile
    Home --> Settings
```

### Complete Login Flow Example

```mermaid
graph TD
    Start((Entry)) --> Splash[Splash Screen]
    Splash --> CheckAuth{Authenticated?}
    CheckAuth -->|Yes| Home[Home Screen]
    CheckAuth -->|No| Login[Login Screen]

    Login --> InputCreds([Enter Credentials])
    InputCreds --> Validate{Valid?}
    Validate -->|Yes| Home
    Validate -->|No| ShowError([Show Error])
    ShowError --> Login

    Login -->|Forgot Password| ForgotPW[Forgot Password]
    ForgotPW --> SendEmail([Send Reset Email])
    SendEmail --> Login

    Login -->|Sign Up| Register[Register Screen]
    Register --> FillForm([Fill Form])
    FillForm --> ValidateForm{Valid?}
    ValidateForm -->|Yes| VerifyEmail[Verify Email]
    ValidateForm -->|No| ShowRegError([Show Error])
    ShowRegError --> Register
    VerifyEmail --> Home

    classDef screen fill:#e8e8e8,stroke:#999,stroke-width:2px
    classDef decision fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    classDef action fill:#d4edda,stroke:#28a745,stroke-width:1px
    class Login,Register,ForgotPW,Home,Splash,VerifyEmail screen
    class CheckAuth,Validate,ValidateForm decision
    class InputCreds,ShowError,SendEmail,FillForm,ShowRegError action
```

### Decision Branches

```mermaid
graph TD
    Screen[Current Screen] --> Action([User Action])
    Action --> Check{Condition?}
    Check -->|Option A| ScreenA[Screen A]
    Check -->|Option B| ScreenB[Screen B]
    Check -->|Option C| ScreenC[Screen C]
```

---

## State Diagram Patterns

### Basic State Transitions

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Loading: Submit
    Loading --> Success: 200 OK
    Loading --> Error: 4xx/5xx
    Error --> Idle: Retry
    Success --> [*]
```

### Nested States

Use nested states for complex screen behaviors:

```mermaid
stateDiagram-v2
    [*] --> FormScreen

    state FormScreen {
        [*] --> Empty
        Empty --> Filling: User Types
        Filling --> Validating: Submit
        Validating --> Invalid: Validation Error
        Validating --> Submitting: Valid
        Invalid --> Filling: Edit
        Submitting --> Success: 200
        Submitting --> ServerError: 5xx
        ServerError --> Filling: Retry
        Success --> [*]
    }
```

### Parallel States

For screens with independent state regions:

```mermaid
stateDiagram-v2
    state Dashboard {
        state "Data Section" as Data {
            [*] --> DataLoading
            DataLoading --> DataLoaded: Fetched
            DataLoading --> DataError: Failed
        }
        --
        state "Notifications" as Notif {
            [*] --> NotifIdle
            NotifIdle --> NotifNew: Push
            NotifNew --> NotifIdle: Dismiss
        }
    }
```

### Auth Flow States Example

```mermaid
stateDiagram-v2
    [*] --> Unauthenticated

    state Unauthenticated {
        [*] --> LoginIdle
        LoginIdle --> Authenticating: Submit Credentials
        Authenticating --> LoginError: Invalid Credentials
        Authenticating --> TokenReceived: Valid Credentials
        LoginError --> LoginIdle: Retry
    }

    TokenReceived --> Authenticated

    state Authenticated {
        [*] --> SessionActive
        SessionActive --> SessionExpiring: Token Near Expiry
        SessionExpiring --> SessionActive: Token Refreshed
        SessionExpiring --> SessionExpired: Refresh Failed
    }

    SessionExpired --> Unauthenticated
    Authenticated --> Unauthenticated: Logout
```

---

## Sequence Diagram Patterns

### Basic Request Flow

```mermaid
sequenceDiagram
    actor User
    participant App as App (Frontend)
    participant API as API Server
    participant DB as Database

    User->>App: Tap Submit
    App->>API: POST /resource
    API->>DB: INSERT INTO resource
    DB-->>API: OK
    API-->>App: 201 Created
    App-->>User: Show Success
```

### Authenticated Request Example

```mermaid
sequenceDiagram
    actor User
    participant App as App (Frontend)
    participant API as API Server
    participant Auth as Auth Service
    participant DB as Database

    User->>App: Enter email + password
    App->>Auth: POST /auth/login {email, password}
    Auth->>DB: SELECT user WHERE email=?
    DB-->>Auth: User record
    Auth->>Auth: Verify password hash

    alt Valid credentials
        Auth-->>App: 200 {accessToken, refreshToken}
        App->>App: Store tokens
        App-->>User: Navigate to Home
    else Invalid credentials
        Auth-->>App: 401 Unauthorized
        App-->>User: Show error message
    end

    Note over App,API: Subsequent authenticated requests

    User->>App: Request data
    App->>API: GET /data (Authorization: Bearer token)
    API->>Auth: Validate token

    alt Token valid
        Auth-->>API: User context
        API->>DB: Query data
        DB-->>API: Results
        API-->>App: 200 {data}
        App-->>User: Display data
    else Token expired
        Auth-->>API: 401
        API-->>App: 401
        App->>Auth: POST /auth/refresh {refreshToken}
        Auth-->>App: 200 {newAccessToken}
        App->>API: Retry GET /data
        API-->>App: 200 {data}
        App-->>User: Display data
    end
```

### Error Handling Pattern

```mermaid
sequenceDiagram
    actor User
    participant App as App (Frontend)
    participant API as API Server

    User->>App: Action
    App->>App: Show loading state
    App->>API: Request

    alt Success
        API-->>App: 200 OK
        App->>App: Update state
        App-->>User: Show result
    else Client Error
        API-->>App: 400/422 {errors}
        App-->>User: Show validation errors
    else Server Error
        API-->>App: 500
        App-->>User: Show generic error + retry
    else Network Error
        App->>App: Timeout/no connection
        App-->>User: Show offline message
    end
```

### Actors Reference

Standard actors for UX flow diagrams:

| Actor | Label | Use |
|-------|-------|-----|
| `actor User` | End user | Human interactions |
| `participant App` | Frontend app | Client-side logic |
| `participant API` | API Server | Backend endpoints |
| `participant Auth` | Auth Service | Authentication |
| `participant DB` | Database | Data persistence |
| `participant Cache` | Cache | Redis/in-memory |
| `participant Queue` | Queue | Async jobs |
| `participant Email` | Email Service | Notifications |

---

## Best Practices

### Diagram Size
- **Max 15-20 nodes** per diagram
- If more complex, split into sub-flows with cross-references
- Use subgraphs to group related screens (max 3-4 subgraphs)

### Splitting Complex Flows

When a flow exceeds 20 nodes:

1. Identify logical boundaries (auth, onboarding, core feature)
2. Create a high-level flow with `[[Sub-flow]]` nodes
3. Create separate detailed diagrams for each sub-flow
4. Link with a note: `See: uc-001/flow-checkout.md`

### Consistent Styling

Define `classDef` once and reuse across all diagrams:

```
classDef screen fill:#e8e8e8,stroke:#999,stroke-width:2px
classDef decision fill:#fff3cd,stroke:#ffc107,stroke-width:2px
classDef action fill:#d4edda,stroke:#28a745,stroke-width:1px
classDef error fill:#f8d7da,stroke:#dc3545,stroke-width:1px
```

### Naming Conventions
- **Screens**: PascalCase — `HomeScreen`, `LoginScreen`
- **Actions**: camelCase verbs — `submitForm`, `loadData`
- **States**: PascalCase — `Loading`, `Error`, `Success`
- **Edges**: Short labels — `Success`, `Fail`, `Tap`, `Submit`

### File Naming
- Use kebab-case: `screen-map.md`, `flow.md`, `states.md`
- Use case folders: `uc-001-registration/`, `uc-002-login/`
