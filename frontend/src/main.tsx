import { createRoot } from 'react-dom/client'
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";

import './index.css'
import App from './App.tsx'

const router = createBrowserRouter([
	{
		path: "/",
		element: <App />
	},
	{
		path: "/hello",
		element: <div> Hello, world! </div>
	}
])

createRoot(document.getElementById('root')!).render(
	<RouterProvider router={router} />
)
