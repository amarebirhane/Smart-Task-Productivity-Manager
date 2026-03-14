import { UserRole } from "@/types/user";

export const roleGuard = {
  isAdmin: (role: UserRole) => role === "admin",
  isManager: (role: UserRole) => role === "manager" || role === "admin",
  canManageTasks: (role: UserRole) => ["admin", "manager"].includes(role),
  canViewAnalytics: (role: UserRole) => ["admin", "manager"].includes(role),
};
