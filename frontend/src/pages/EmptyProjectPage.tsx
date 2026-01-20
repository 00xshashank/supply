import { IconFolderCode } from "@tabler/icons-react"
import { ArrowUpRightIcon } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
Empty,
EmptyContent,
EmptyDescription,
EmptyHeader,
EmptyMedia,
EmptyTitle,
} from "@/components/ui/empty"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { toast } from "sonner"
import { useNavigate } from "react-router"

const backendURL = "http://localhost:8000"

export default function EmptyDemo() {
	const [projectName, setProjectName] = useState<string>("")
	const [isModalOpen, setModalOpen] = useState<boolean>(false)

	const navigate = useNavigate()

	function toggleModal() {
		console.log("Toggled")
		setModalOpen(true)
	}

	async function createProject() {
		console.log("Creating with project name: ", projectName)
		toast.info("Creating project...")

		const createProjectResponse = await fetch(`${backendURL}/api/create-project/`, {
			method: 'POST',
			credentials: "include",
			headers: {
				'Content-Type': 'application/json',
			}, 
			body: JSON.stringify({
				"name": projectName
			})
		})
		const createJson = await createProjectResponse.json()
		if ("status" in createJson) {
			if (createJson["status"] === "success") {
				const setResponse = await fetch(`${backendURL}/api/select-project/`, {
					credentials: "include",
					headers: {
						'Content-Type': 'application/json',
					}, 
					body: JSON.stringify({
						"name": projectName
					})
				})
				const setJson = await setResponse.json()
				if ("status" in setJson) {
					if (setJson["status"] === "success") {
						navigate('/first-chat')
					} else {
						toast.error(setJson['message'])
					}
				} else {
					toast.error("Malformed response from server, try again later")
				}
			} else {
				if ("message" in createJson) {
					toast.error(createJson['message'])
				} else {
					toast.error("Malformed response from server, try again later")
				}
			}
		} else {
			toast.error("Malformed response from server, try again later")
		}
	}

	return (
		<>
		<Empty>
			<EmptyHeader>
			<EmptyMedia variant="icon">
				<IconFolderCode />
			</EmptyMedia>
			<EmptyTitle>No Projects Yet</EmptyTitle>
			<EmptyDescription>
				You haven&apos;t created any projects yet. Get started by creating
				your first project.
			</EmptyDescription>
			</EmptyHeader>
			<EmptyContent>
			<div className="flex gap-2">
				<Button onClick={toggleModal}>Create Project</Button>
			</div>
			</EmptyContent>
			<Button
			variant="link"
			asChild
			className="text-muted-foreground"
			size="sm"
			>
			<a href="#">
				Learn More <ArrowUpRightIcon />
			</a>
			</Button>
		</Empty>
		{ isModalOpen && 
		<div id="modal-overlay" 
		className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 flex items-center justify-center"
		onClick={() => setModalOpen(false)}>
			<Card className="w-sm" onClick={(e) => {e.stopPropagation(); setModalOpen(true);}}>
				<CardHeader>
					<CardTitle>Enter project name:</CardTitle>
				</CardHeader>
				<CardContent className="flex flex-row">
					<Input value={projectName} onChange={(e) => {setProjectName(e.target.value)}} />
					<Button onClick={createProject}><ArrowUpRightIcon /></Button>
				</CardContent>
			</Card>
		</div>}
		</>
	)
}
