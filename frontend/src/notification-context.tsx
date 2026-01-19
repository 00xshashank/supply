import React, { useContext, createContext, useState, useCallback } from "react";
import { generateRandomId } from "@/lib/generate-utils"

type NotificationType = "error" | "warning" | "info" | "success"

export interface Notification {
    id: string,
    message: string,
    type: NotificationType
}

interface NotificationContextType {
    notifications: Notification[],
    addNotification: (message: string, type: NotificationType) => (() => void),
    removeNotification: (id: string) => void
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined)

export function NotificationProvider({ children } : { children: React.ReactNode }) {
    const [ notifications, setNotifications ]  = useState<Notification[]>([])
    const id = generateRandomId(10) 
    const addNotification = (message: string, type: NotificationType) => {
        const newNotification: Notification = {
            id,
            message,
            type
        }

        setNotifications(prev => [...prev, newNotification])

        const timer = setTimeout(() => {
            removeNotification(id)
        }, 5000)

        return () => clearTimeout(timer)
    }

    const removeNotification = useCallback((id: string) => {
        setNotifications(prev => prev.filter((notification) => notification.id !== id))
    }, [])

    return (
        <NotificationContext.Provider value={{ notifications, addNotification, removeNotification }}>
            {children}
        </NotificationContext.Provider>
    )
}

export function useNotification() {
    const context = createContext(NotificationContext)
    if (!context) {
        throw new Error("useNotification must only be used within a NotificationContext")
    }
    return context
}