import { useEffect, useState } from "react"
import { toast } from "sonner"
import { useNavigate } from "react-router"

import EmptyDemo from "./EmptyProjectPage"

const backendURL = "http://localhost:8000"

export function DashboardPage() {
    const [projectsList, setProjectsList] = useState<Array<string>>([]);
    
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

    return (
        <>
        {projectsList.length===0 && <EmptyDemo />}
        {projectsList.length!==0 && <div>{projectsList}</div>}
        </>
    )
}