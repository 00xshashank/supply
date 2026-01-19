import { createRoot } from 'react-dom/client'
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";
import { Toaster } from "@/components/ui/sonner"

import './index.css'
import App from './App.tsx'
import Login from './pages/Login.tsx';
import SignUp from './pages/Signup.tsx';
import { DashboardPage } from './pages/Dashboard.tsx';
import FirstChatPage from './pages/FirstChatPage.tsx';
import ProgressPage from './pages/ProgressPage.tsx';

const router = createBrowserRouter([
	{
		path: "/",
		element: <App />
	},
	{
		path: "/login",
		element: <Login /> 
	},
	{
		path: "/signup",
		element: <SignUp />
	},
	{
		path: "/dashboard",
		element: <DashboardPage />
	},
	{
		path: "/first-chat",
		element: <FirstChatPage />
	},
	{
		path: "/progress",
		element: <ProgressPage />
	}
])

createRoot(document.getElementById('root')!).render(
	<>
		<RouterProvider router={router} />
		<Toaster />
	</>
)
