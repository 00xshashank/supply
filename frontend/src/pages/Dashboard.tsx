import React, { useEffect, useState } from "react"
import { toast } from "sonner"
import { useNavigate } from "react-router"

import EmptyDemo from "./EmptyProjectPage"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import {
  ArrowBigRight,
  ArrowUpRightIcon,
  Plus,
  Activity,
  Network,
} from "lucide-react"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

const backendURL = "http://localhost:8000"

export function DashboardPage() {
  const [projectsList, setProjectsList] = useState<Array<string>>([])
  const [username, setUsername] = useState<string>("")
  const [projectName, setProjectName] = useState<string>("")
  const [isModalOpen, setModalOpen] = useState<boolean>(false)

  const navigate = useNavigate()

  useEffect(() => {
    async function fetchData() {
      const authResponse = await fetch(`${backendURL}/api/is-authenticated/`, {
        credentials: "include",
      })
      const authData = await authResponse.json()
      if (authData.status !== true) navigate("/login")

      const projectListData = await fetch(`${backendURL}/api/get-projects/`, {
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      })
      const projectListJson = await projectListData.json()

      if (projectListJson.status === "success") {
        setProjectsList(projectListJson.message)
        setUsername(projectListJson.name)
      } else {
        toast.error(projectListJson.message)
      }
    }

    fetchData()
  }, [])

  async function createProject() {
    if (!projectName.trim()) return toast.error("Enter a project name")
    toast.info("Creating project...")

    const createProjectResponse = await fetch(
      `${backendURL}/api/create-project/`,
      {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: projectName }),
      }
    )
    const createJson = await createProjectResponse.json()

    if (createJson.status === "success") {
      await selectAndNavigate(projectName, "/first-chat")
    } else {
      toast.error(createJson.message || "Failed to create project")
    }
  }

  // 🔹 Reusable function for all navigation
  async function selectAndNavigate(projectName: string, route: string) {
    const setResponse = await fetch(`${backendURL}/api/select-project/`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: projectName }),
    })
    const responseJson = await setResponse.json()

    if (responseJson.status === "failure") {
      toast.error("Failed to open project")
      return
    }

    navigate(route)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {projectsList.length === 0 && <EmptyDemo />}

      {projectsList.length !== 0 && (
        <div className="max-w-5xl mx-auto px-6 py-10">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-2xl font-semibold text-gray-800">
                Welcome back, {username}
              </h1>
              <p className="text-gray-500">
                Select a project to continue
              </p>
            </div>
            <Button onClick={() => setModalOpen(true)}>
              <Plus className="mr-2 h-4 w-4" />
              Create Project
            </Button>
          </div>

          {/* Projects Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projectsList.map((project) => (
              <Card
                key={project}
                className="hover:shadow-md transition"
              >
                <CardHeader>
                  <CardTitle className="flex justify-between items-center">
                    <span>{project}</span>
                    {/* Primary action */}
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={() =>
                        selectAndNavigate(project, "/first-chat")
                      }
                    >
                      <ArrowBigRight />
                    </Button>
                  </CardTitle>
                </CardHeader>

                <CardContent className="space-y-4">
                  <p className="text-sm text-gray-500">
                    Continue working on this project.
                  </p>

                  {/* Secondary actions */}
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="flex-1"
                      onClick={() =>
                        selectAndNavigate(project, "/status")
                      }
                    >
                      <Activity className="mr-2 h-4 w-4" />
                      Status
                    </Button>

                    <Button
                      variant="outline"
                      size="sm"
                      className="flex-1"
                      onClick={() =>
                        selectAndNavigate(project, "/graph")
                      }
                    >
                      <Network className="mr-2 h-4 w-4" />
                      Graph
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Modal */}
      {isModalOpen && (
        <div
          className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 flex items-center justify-center"
          onClick={() => setModalOpen(false)}
        >
          <Card
            className="w-[400px]"
            onClick={(e) => e.stopPropagation()}
          >
            <CardHeader>
              <CardTitle>Create new project</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Project name</Label>
                <Input
                  placeholder="e.g. Supply Chain AI"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                />
              </div>
              <Button className="w-full" onClick={createProject}>
                Create & Open
                <ArrowUpRightIcon className="ml-2 h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
