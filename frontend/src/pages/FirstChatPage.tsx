import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { useState, useEffect, useRef } from "react"
import { ArrowBigRight, LoaderCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useNavigate } from "react-router"
import { toast } from "sonner"

const backendURL = "http://localhost:8000"

type Message = {
  role: "assistant" | "user"
  content: string
}

type ChatsRendererProps = {
  messages: Array<Message>
}

export default function FirstChatPage() {
  const [messages, setMessages] = useState<Array<Message>>([])
  const [userInput, setUserInput] = useState<string>("")
  const [isLoading, setLoading] = useState<boolean>(false)
  const navigate = useNavigate()
  const bottomRef = useRef<HTMLDivElement | null>(null)

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  useEffect(() => {
    async function fetchChat() {
      const chatsResponse = await fetch(`${backendURL}/api/get-chats`, {
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      })

      const chatsJson = await chatsResponse.json()

      if (chatsJson.status === "success") {
        const chatsState = chatsJson.message.map(
          (m: { role: "user" | "assistant"; content: string }) => ({
            role: m.role,
            content: m.content,
          })
        )
        setMessages(chatsState)
      } else {
        toast.error("Failed to fetch previous chats.")
      }
    }

    fetchChat()
  }, [])

  async function askQuestion() {
    if (!userInput.trim()) return

    const newMessages: Array<Message> = [
      ...messages,
      { role: "user", content: userInput },
    ]
    setMessages(newMessages)
    setLoading(true)

    const agentResponse = await fetch(`${backendURL}/api/first-chat/`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput }),
    })

    const responseJson = await agentResponse.json()

    if (responseJson.status === "failure" && responseJson.text === "not logged in") {
      navigate("/login")
    }

    if (responseJson.status === "success") {
      setMessages([
        ...newMessages,
        { role: "assistant", content: responseJson.message },
      ])
    }

    if (responseJson.status === "completed") {
      toast.success("Information extracted successfully.")
      navigate("/progress")
    }

    setUserInput("")
    setLoading(false)
  }

  return (
    <div className="h-screen w-full bg-gray-50 flex justify-center">
      <div className="w-full max-w-3xl flex flex-col">
        
        {/* Header */}
        <div className="p-4 border-b bg-white shadow-sm">
          <h1 className="text-xl font-semibold text-gray-800">
            AI Assistant
          </h1>
        </div>

        {/* Chat area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <ChatsRenderer messages={messages} />
          <div ref={bottomRef} />
        </div>

        {/* Input bar */}
        <div className="p-4 border-t bg-white flex gap-2">
          <Input
            type="text"
            placeholder="Type your message..."
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && askQuestion()}
            className="flex-1"
          />
          <Button onClick={askQuestion} disabled={isLoading}>
            {isLoading ? (
              <LoaderCircle className="animate-spin" />
            ) : (
              <ArrowBigRight />
            )}
          </Button>
        </div>
      </div>
    </div>
  )
}

function ChatsRenderer({ messages }: ChatsRendererProps) {
  return (
    <>
      {messages.map((m, idx) => (
        <div
          key={idx}
          className={`flex ${
            m.role === "user" ? "justify-end" : "justify-start"
          }`}
        >
          <Card
            className={`
              max-w-[70%] px-4 py-3 text-sm shadow-sm
              ${
                m.role === "user"
                  ? "bg-blue-600 text-white rounded-2xl rounded-br-sm"
                  : "bg-white text-gray-800 rounded-2xl rounded-bl-sm border"
              }
            `}
          >
            {m.content}
          </Card>
        </div>
      ))}
    </>
  )
}
