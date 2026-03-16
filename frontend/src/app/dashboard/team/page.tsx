"use client";

import React, { useState, useEffect } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import api from "@/services/api";
import { Users, TrendingUp, CheckSquare, Clock } from "lucide-react";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line
} from "recharts";

const teamEfficiencyData = [
  { day: "Mon", score: 85 },
  { day: "Tue", score: 92 },
  { day: "Wed", score: 88 },
  { day: "Thu", score: 95 },
  { day: "Fri", score: 90 },
];

export default function TeamDashboard() {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get("/analytics/system");
        setAnalytics(res.data);
      } catch (error) {
        console.error("Failed to fetch team dashboard data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <ProtectedRoute allowedRoles={["manager", "admin"]}>
      <div className="space-y-8 animate-fade-in">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Team Productivity</h1>
          <p className="text-sm text-slate-500">Track and optimize your team's velocity</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card-premium p-6 border-l-4 border-l-blue-500">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-50 rounded-xl text-blue-600">
                <Users className="h-6 w-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500">Active Team Members</p>
                <h3 className="text-2xl font-bold text-slate-900">
                  {loading ? "..." : analytics?.total_users || 0}
                </h3>
              </div>
            </div>
          </div>
          <div className="card-premium p-6 border-l-4 border-l-emerald-500">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-emerald-50 rounded-xl text-emerald-600">
                <CheckSquare className="h-6 w-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500">Total Tasks in System</p>
                <h3 className="text-2xl font-bold text-slate-900">
                  {loading ? "..." : analytics?.total_tasks || 0}
                </h3>
              </div>
            </div>
          </div>
          <div className="card-premium p-6 border-l-4 border-l-purple-500">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-purple-50 rounded-xl text-purple-600">
                <TrendingUp className="h-6 w-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500">Avg. Task Velocity</p>
                <h3 className="text-2xl font-bold text-slate-900">1.4 days</h3>
              </div>
            </div>
          </div>
        </div>

        <div className="card-premium p-6">
          <h3 className="text-lg font-bold text-slate-900 mb-6 font-premium">Team Efficiency Trend</h3>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={teamEfficiencyData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{ fill: "#64748b" }} />
                <YAxis axisLine={false} tickLine={false} tick={{ fill: "#64748b" }} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                />
                <Line 
                  type="monotone" 
                  dataKey="score" 
                  stroke="#0ea5e9" 
                  strokeWidth={3} 
                  dot={{ r: 6, fill: "#0ea5e9", strokeWidth: 2, stroke: "#fff" }}
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
