"use client";

import TaskList from "@/features/tasks/TaskList";

export default function MyTasksPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3 mb-2">
        <div className="h-8 w-1 bg-primary-600 rounded-full"></div>
        <h2 className="text-xl font-bold text-slate-800">My Productivity Hub</h2>
      </div>
      <TaskList />
    </div>
  );
}
