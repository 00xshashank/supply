import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { ArrowBigRight, LoaderCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useNavigate } from "react-router"

const backendURL = "http://localhost:8000"

type Message = {
    role: "assistant" | "user"
    content: String
}

type ChatsRendererProps = {
    messages: Array<Message>
}

export default function FirstChatPage() {
    const [messages, setMessages] = useState<Array<Message>>([]);
    const [userInput, setUserInput] = useState<string>("");
    const [isLoading, setLoading] = useState<boolean>(false);

    const navigate = useNavigate();

    async function askQuestion() {
        setMessages([...messages, {
            role: "user",
            content: userInput
        }])
        setUserInput("")
        setLoading(true)
        
        const agentResponse = await fetch(`${backendURL}/api/first-chat`, {
            method: 'POST',
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(messages)
        })
        const responseJson = await agentResponse.json()
        if (responseJson.status === "failure" && responseJson.text === "not logged in") {
            navigate('/login')
        }
        if (responseJson.status === "success") {
            setMessages([...messages, {
                role: "assistant",
                content: responseJson.message
            }])
        }
        if (responseJson.status === "completed") {
            navigate('/progress')
        }

        setLoading(false)
    }

    return (
        <>
        <div className="flex flex-col items-center">
            <ChatsRenderer messages={messages}/>
            <div className="flex flex-row">
                <Input
                    type="text"
                    value={userInput}
                    onChange={(e) => {setUserInput(e.target.value)}}
                />
                <Button onClick={askQuestion}>
                    {isLoading && <LoaderCircle />}
                    {!isLoading && <ArrowBigRight />}
                </Button>
            </div>
        </div>
        </>
    )
}

function ChatsRenderer({ messages }: ChatsRendererProps) {
    return (
        <>
        {messages.map((m) => {
            return (
            <>
                {m.role === "assistant" &&
                    <Card className="p-4 pr-8 m-1 bg-black text-white flex justify-start">
                        <p className="text-md">{m.content}</p>
                    </Card>
                }
                {m.role === "user" &&
                    <Card className="p-4 m-1 pl-8 bg-white text-black flex justify-end">
                        <p className="text-md">{m.content}</p>
                    </Card>
                }
            </>
            )
        })}
        </>
    )
}