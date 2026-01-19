import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useState } from "react"
import { Link } from "react-router"
import { z } from "zod"
import { toast } from "sonner"

const SignUpResponse = z.object({
  status: z.enum(["failure", "success"]),
  message: z.string(),
})

const emailSchema = z.string().email("Please enter a valid email address.")

const BACKEND_URL = "http://localhost:8000"

export default function SignUp() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [password2, setPassword2] = useState("")
  const [email, setEmail] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  async function createUser() {
    let hasError = false

    if (!emailSchema.safeParse(email).success) {
      toast.error("Please enter a valid email address.")
      hasError = true
    }

    if (username.length < 6) {
      toast.error("Username must be at least 6 characters long.")
      hasError = true
    }

    if (password.length < 8) {
      toast.error("Password must be at least 8 characters long.")
      hasError = true
    }

    if (password !== password2) {
      toast.error("Passwords do not match.")
      hasError = true
    }

    if (hasError) return

    setIsLoading(true)

    try {
      console.log("[v0] Fetching CSRF token from:", `${BACKEND_URL}/api/csrf`)
      const cookieResponse = await fetch(`${BACKEND_URL}/api/csrf`, {
        credentials: "include",
      })

      console.log("[v0] CSRF response status:", cookieResponse.status)

      if (!cookieResponse.ok) {
        toast.error("Failed to fetch CSRF token.")
        setIsLoading(false)
        return
      }

      const csrfToken = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1]

      console.log("[v0] CSRF token found:", !!csrfToken)

      if (!csrfToken) {
        toast.error("CSRF token not found.")
        setIsLoading(false)
        return
      }

      console.log("[v0] Sending signup request to:", `${BACKEND_URL}/api/signup/`)
      const response = await fetch(`${BACKEND_URL}/api/signup/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
          username,
          password,
          email,
        }),
      })

      console.log("[v0] Signup response status:", response.status)

      const data = await response.json()
      console.log("[v0] Signup response data:", data)

      const parsed = SignUpResponse.safeParse(data)

      if (!parsed.success) {
        toast.error("Invalid response from server.")
        setIsLoading(false)
        return
      }

      if (parsed.data.status === "failure") {
        toast.error(parsed.data.message)
      } else {
        toast.success(parsed.data.message)

        setUsername("")
        setPassword("")
        setPassword2("")
        setEmail("")
      }
    } catch (err) {
      console.error("[v0] Sign up error:", err)
      toast.error("Could not connect to the server.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Create a new account</CardTitle>
          <CardDescription>Enter your details below to create your account</CardDescription>
          <div className="mt-4">
            <Button variant="link" className="p-0">
              <Link to="/login">Already have an account? Log In</Link>
            </Button>
          </div>
        </CardHeader>

        <CardContent>
          <div className="flex flex-col gap-6">
            <div className="flex flex-col gap-3">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                disabled={isLoading}
              />
            </div>
            <div className="flex flex-col gap-3">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                disabled={isLoading}
              />
            </div>
            <div className="flex flex-col gap-3">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="At least 8 characters"
                disabled={isLoading}
              />
            </div>
            <div className="flex flex-col gap-3">
              <Label htmlFor="password2">Confirm Password</Label>
              <Input
                id="password2"
                type="password"
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                placeholder="Confirm your password"
                disabled={isLoading}
              />
            </div>
          </div>
        </CardContent>

        <CardFooter>
          <Button className="w-full" onClick={createUser} disabled={isLoading}>
            {isLoading ? "Creating account..." : "Sign Up"}
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
