import { createRoot } from 'react-dom/client'
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";

import './index.css'
import App from './App.tsx'
import Login from './Login.tsx';
import SignUp from './Signup.tsx';

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
	}
])

createRoot(document.getElementById('root')!).render(
	<RouterProvider router={router} />
)
