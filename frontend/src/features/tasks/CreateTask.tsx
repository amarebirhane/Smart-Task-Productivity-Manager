"use client";

import React, { useState } from "react";
import { Plus, X, Loader2 } from "lucide-react";
import { useTasks } from "@/hooks/useTasks";

export default function CreateTask({ onTaskCreated }: { onTaskCreated?: () => void }) {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const { addTask } = useTasks();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    try {
      await addTask({ title, priority: "medium", status: "pending" });
      setTitle("");
      setIsOpen(false);
      if (onTaskCreated) onTaskCreated();
    } catch (error) {
      console.error("Failed to create task", error);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="btn-primary flex items-center gap-2 group"
      >
        <Plus className="h-4 w-4 group-hover:rotate-90 transition-transform" />
        New Task
      </button>
    );
  }

  return (
    <div className="card-premium p-4 border-primary-200 bg-primary-50/30">
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <div className="flex justify-between items-center">
          <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Quick Create</h3>
          <button type="button" onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-slate-600">
            <X className="h-4 w-4" />
          </button>
        </div>
        <input
          autoFocus
          className="input-base"
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={loading}
        />
        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={() => setIsOpen(false)}
            className="px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-all"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading || !title.trim()}
            className="px-4 py-1.5 text-xs font-bold bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-all disabled:opacity-50"
          >
            {loading ? <Loader2 className="h-3 w-3 animate-spin" /> : "Create Task"}
          </button>
        </div>
      </form>
    </div>
  );
}
