import React, { useEffect, useState } from "react"
import { toast } from "sonner"
import { useNavigate } from "react-router"

import EmptyDemo from "./EmptyProjectPage"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { ArrowBigRight } from "lucide-react"

const backendURL = "http://localhost:8000"

export function DashboardPage() {
    const [projectsList, setProjectsList] = useState<Array<string>>([]);
    const [username, setUsername] = useState<string>("")
    
    const navigate = useNavigate()
    
    useEffect(() => {
        async function fetchData() {
            const authResponse = await fetch(`${backendURL}/api/is-authenticated/`, {
                credentials: "include"
            })
            const authData = await authResponse.json()
            console.log(authData)
            if ("status" in authData) {
                if (authData["status"] !== true) {
                    navigate('/login')
                }
            } else {
                toast.error("Server returned malformed response. Please try again later.")
                return
            }

            const projectListData = await fetch(`${backendURL}/api/get-projects/`, {
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            const projectListJson = await projectListData.json()
            if ("status" in projectListJson) {
                if (projectListJson["status"] === "success") {
                    setProjectsList(projectListJson['message'])
                    setUsername(projectListJson['name'])
                } else {
                    toast.error(projectListJson['message'])
                }
            } else {
                toast.error("Server returned malformed response, try again later")
                return
            }

            console.log(projectListJson)
        }

        fetchData()
    }, [])

    const selectProject = async (event: React.MouseEvent<HTMLButtonElement>) => {
        const buttonId = event.target.id ?? null
        console.log(buttonId)

        if (buttonId !== null) {
            const setResponse = await fetch(`${backendURL}/api/select-project/`, {
                method: "POST",
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "name": buttonId
                })
            })
            const responseJson = await setResponse.json()
            if (responseJson.status === "failure") {
                if (responseJson.text === "Please log in first") {
                    navigate('/login')
                } else {
                    toast.error("An error occurred, please try again later.")
                }
                return
            }
            navigate('/first-chat')            
        } else {
            toast.error("Something went wrong.")
        }
    };

    return (
        <>
        {projectsList.length===0 && <EmptyDemo />}
        {projectsList.length!==0 && 
            <>
            <div>
                Hi, {username}!
            </div>
            { projectsList.map((project) => {
                return (
                    <div id={project} className="flex flex-row">
                    <Label>
                        {project}
                    </Label>
                    <Button id={project} onClick={selectProject}><ArrowBigRight /></Button>
                    </div>
                )
            })}
            </>
        }
        </>
    )
}