import { Button } from "@/components/ui/button"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useState } from "react"

import { Link } from "react-router"
import { z } from "zod"

const SignUpResponse = z.object({
    status: z.enum(["failure", "success"]),
    message: z.string()
})

const BACKEND_URL = "http://localhost:8000"

export default function SignUp() {
    const [ username, setUsername ] = useState<string>("")
    const [ password, setPassword ] = useState<string>("")
    const [ password2, setPassword2 ] = useState<string>("")
    const [ email, setEmail ] = useState<string>("")

    async function createUser() {
        let error: boolean = false
        if (username.length <= 6) {
            console.error("Username must be at least 6 character long.")
            error = true
        }
        if (password.length < 8) {
            console.error("Please provide a password greater than 8 characters long.")
            error = true
        }
        if (password !== password2) {
            console.error("Passwords do not match.")
            error = true
        }
        
        if (!error) {
            const cookieResponse = await fetch(`${BACKEND_URL}/api/csrf`)
            if (cookieResponse.status !== 200) {
                console.error("Failed to fetch CSRF token.")
                return
            }

            const cookieValue = document.cookie
            const csrfToken = cookieValue.split('=').pop()
            console.log("Cookie is: ", csrfToken)
            const response = await fetch(`${BACKEND_URL}/api/signup/`, {
                method: 'POST',
                credentials: "include",
                headers: {
                    "Content-type": "application/json",
                    "X-CSRFToken": csrfToken!
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    email: email
                })
            })
            const data = await response.json()
            console.log(data)

            const parsedResult = SignUpResponse.safeParse(data)
            if (parsedResult.error) {
                console.error("Error while parsing data from backend")
                return
            }
            const parsedData = parsedResult.data
            if (parsedData.status === "failure") {
                console.error(parsedData.message)
            } else {
                console.log(parsedData.message)
            }
        }

        setEmail("")
        setUsername("")
        setPassword("")
        setPassword2("")
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
                    <Label>Email</Label>
                    <Input value={email} onChange={(e) => { setEmail(e.target.value) }}/>
                </div>
                <div className="flex flex-col gap-3">
                    <Label>Password</Label>
                    <Input value={password} type="password" onChange={(e) => { setPassword(e.target.value) }}/>
                </div>
                <div className="flex flex-col gap-3">
                    <Label>Confirm Password</Label>
                    <Input value={password2} type="password" onChange={(e) => { setPassword2(e.target.value) }}/>
                </div>
            </div>
        </CardContent>
        <CardFooter className="flex-col gap-2">
            <Button type="submit" className="w-full" onClick={createUser}>
            Sign Up
            </Button>
        </CardFooter>
        </Card>
        </div>
    )
}
