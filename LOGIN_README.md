# RecruiterIQ Login System

A modern, responsive login system built with Vue.js + Vuetify frontend and FastAPI backend.

## Features

- ✨ Clean, modern UI with Vuetify Material Design
- 🔐 JWT-based authentication
- 🛡️ Route guards for protected pages
- 📱 Fully responsive design
- 🎨 Smooth animations and transitions
- 💾 Persistent login state

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## Usage

1. **Landing Page**: Visit `http://localhost:5173` - displays welcome page with "Get Started" button
2. **Login Page**: Click "Get Started" or visit `/login` directly
3. **Authentication**: Use the default admin credentials:
   - Email: `admin@recruiteriq.com`
   - Password: `admin123`
4. **Protected Route**: After login, you'll be redirected to `/protected` (the dashboard)

## Architecture

### Frontend (Vue.js + Vuetify)
- **Pages**: Login, Protected Dashboard, Landing
- **Store**: Pinia-based auth store with token management
- **Router**: Vue Router with authentication guards
- **Styling**: Vuetify Material Design with custom gradients

### Backend (FastAPI)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Database**: SQLAlchemy with user management
- **CORS**: Configured for frontend communication
- **Auto-admin**: Creates default admin user on startup

## File Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── index.vue      # Landing page
│   │   ├── login.vue      # Login form
│   │   └── protected.vue  # Dashboard
│   ├── stores/
│   │   └── auth.js        # Authentication store
│   └── router/
│       └── index.js       # Router with guards

backend/
├── main.py               # FastAPI app with CORS
├── auth.py               # JWT & auth logic
├── database.py           # SQLAlchemy models
└── models.py             # Pydantic models
```

## Key Features Explained

### 🎨 Modern Design
- Glassmorphism login card with subtle backdrop blur
- Gradient backgrounds that adapt to light/dark themes
- Clean, minimal interface with proper spacing
- Smooth hover effects and transitions

### 🔐 Security
- JWT token-based authentication
- Secure password hashing with bcrypt
- Token validation on protected routes
- Automatic logout on token expiry

### 📱 Responsive
- Mobile-first design approach
- Flexible grid layout with Vuetify
- Touch-friendly interactive elements
- Consistent experience across devices

### 🚀 Performance
- Minimal bundle size with Vue 3 Composition API
- Lazy loading of components
- Efficient state management with Pinia
- Fast development server with Vite

## Customization

The design is built to be easily customizable:

- **Colors**: Modify Vuetify theme in `src/plugins/vuetify.js`
- **Layout**: Update card sizing and positioning in login.vue
- **Branding**: Replace logo and app name throughout components
- **API Endpoint**: Update base URL in `src/stores/auth.js`

## Troubleshooting

- Ensure both frontend and backend servers are running
- Check browser console for any CORS or network errors
- Verify the admin user exists in the database
- Make sure ports 8000 and 5173 are available