import { useEffect, useState } from "react"
import {
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardAction,
    CardContent,
    CardFooter
} from "@/components/ui/card"
import { Button } from "./components/ui/button"
import { Label } from "./components/ui/label"
import { Input } from "./components/ui/input"

import { Link } from "react-router"
import { z } from "zod"

const LogInResponse = z.object({
    status: z.enum(["failure", "success"]),
    message: z.string()
})

const BACKEND_URL = "http://localhost:8000"

export default function Login() {
    const [ username, setUsername ] = useState<string>("")
    const [ password, setPassword ] = useState<string>("")

    useEffect(() => {
        async function fetchCookie() {
            const res = await fetch(`${BACKEND_URL}/api/csrf`, {
                credentials: "include"
            })
            const data = await res.json()
            console.log(data)
        }

        fetchCookie()
    }, [])

    async function validateUser() {
        let error: boolean = false
        const response = await fetch(`${BACKEND_URL}/api/csrf`, {
            credentials: "include"
        })
        if (response.status !== 200) {
            console.error("Failed to fetch CSRF token")
            return
        }
        const cookieValue = document.cookie
        const csrfToken = cookieValue.split('=').pop()

        if (username.length <= 6) {
            console.error("Please enter a valid username")
            error = true
        }
        if (password.length <= 8) {
            console.error("Please enter a valid password")
            error = true
        }

        if (!error) {
            const loginResponse = await fetch(`${BACKEND_URL}/api/login/`, {
                credentials: "include",
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                    "X-CSRFToken": csrfToken!
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            })
            const data = await loginResponse.json()
            console.log(data)

            const parsedResult = LogInResponse.safeParse(data)
            if (parsedResult.error) {
                console.error("Error while parsing response body")
            }
            if (parsedResult.data?.message == "failure") {
                console.error("Log in failed")
            } else {
                console.log("Log in attempt successful")
            }
        }

        setUsername("")
        setPassword("")
    }

    return (
        <div className="flex min-h-screen items-center justify-center">
        <Card className="w-full max-w-md">
        <CardHeader>
            <CardTitle>Create a new account</CardTitle>
            <CardDescription>
            Enter your details below to create your account
            </CardDescription>
            <CardAction>
            <Button variant="link">
                <Link to='/login' className="flex gap-1 flex-row flex-start">
                    Log In
                </Link>
            </Button>
            </CardAction>
        </CardHeader>
        <CardContent>
            <div className="flex flex-col gap-6">
                <div className="flex flex-col gap-3">
                    <Label>Username</Label>
                    <Input value={username} onChange={(e) => { setUsername(e.target.value) }}/>
                </div>
                <div className="flex flex-col gap-3">
                    <Label>Password</Label>
                    <Input value={password} type="password" onChange={(e) => { setPassword(e.target.value) }}/>
                </div>
            </div>
        </CardContent>
        <CardFooter className="flex-col gap-2">
            <Button type="submit" className="w-full" onClick={validateUser}>
            Sign Up
            </Button>
        </CardFooter>
        </Card>
        </div>
    )
}