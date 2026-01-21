import { useState } from "react"
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardContent,
  CardFooter,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Link, useNavigate } from "react-router"
import { z } from "zod"
import { toast } from "sonner"

const LogInResponse = z.object({
  status: z.enum(["failure", "success"]),
  message: z.string(),
})

const BACKEND_URL = "http://localhost:8000"

export default function Login() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()

  // useEffect(() => {
  //   fetch(`${BACKEND_URL}/api/csrf`, {
  //     credentials: "include",
  //   }).catch(() => {
  //     toast.error("Failed to initialize CSRF protection.")
  //   })
  // }, [])

  async function validateUser() {
    let hasError = false

    if (username.length < 6) {
      toast.error("Please enter a valid username.")
      hasError = true
    }

    if (password.length < 8) {
      toast.error("Please enter a valid password.")
      hasError = true
    }

    if (hasError) return

    try {
      // const csrfToken = document.cookie
      //   .split("; ")
      //   .find((row) => row.startsWith("csrftoken="))
      //   ?.split("=")[1]

      // if (!csrfToken) {
      //   toast.error("CSRF token missing.")
      //   return
      // }

      toast.loading("Logging in…", { id: "login" })

      const response = await fetch(`${BACKEND_URL}/api/login/`, {
        credentials: "include",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      })

      const data = await response.json()
      console.log(data)
      const parsed = LogInResponse.safeParse(data)

      if (!parsed.success) {
        toast.error("Invalid server response.", { id: "login" })
        return
      }

      if (parsed.data.status === "failure") {
        toast.error(parsed.data.message || "Login failed.", {
          id: "login",
        })
      } else {
        toast.success(parsed.data.message || "Login successful!", {
          id: "login",
        })

        setUsername("")
        setPassword("")

        navigate("/dashboard")
      }
    } catch (err) {
      console.error(err)
      toast.error("Unable to connect to server.", { id: "login" })
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Log in to your account</CardTitle>
          <CardDescription>
            Enter your credentials to continue
          </CardDescription>
          <CardAction>
            <Button variant="link">
              <Link to="/signup">Sign Up</Link>
            </Button>
          </CardAction>
        </CardHeader>

        <CardContent>
          <div className="flex flex-col gap-6">
            <div className="flex flex-col gap-3">
              <Label>Username</Label>
              <Input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="flex flex-col gap-3">
              <Label>Password</Label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
        </CardContent>

        <CardFooter>
          <Button className="w-full" onClick={validateUser}>
            Log In
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
