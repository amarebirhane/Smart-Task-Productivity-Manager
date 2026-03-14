"use client";

import React, { useState } from "react";
import { authService } from "@/features/auth/authService";
import AuthenticatedLayout from "@/components/AuthenticatedLayout";
import { Lock, Loader2, KeyRound } from "lucide-react";

export default function ChangePasswordPage() {
  const [formData, setFormData] = useState({
    old_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: "", text: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.new_password !== formData.confirm_password) {
      setMessage({ type: "error", text: "New passwords do not match." });
      return;
    }

    setLoading(true);
    setMessage({ type: "", text: "" });

    try {
      await authService.changePassword({
        old_password: formData.old_password,
        new_password: formData.new_password,
      });
      setMessage({ type: "success", text: "Password changed successfully!" });
      setFormData({ old_password: "", new_password: "", confirm_password: "" });
    } catch (err: any) {
      setMessage({ 
        type: "error", 
        text: err.response?.data?.detail || "Failed to change password." 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthenticatedLayout>
      <div className="max-w-2xl mx-auto py-8 px-4">
        <div className="flex items-center space-x-4 mb-8">
          <div className="h-16 w-16 bg-yellow-100 rounded-full flex items-center justify-center text-yellow-600">
            <Lock size={32} />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Security Setting</h1>
            <p className="text-slate-500">Update your account password</p>
          </div>
        </div>

        <div className="card-premium p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {message.text && (
              <div className={`p-4 rounded-lg text-sm ${
                message.type === "success" ? "bg-green-50 text-green-700 border border-green-100" : "bg-red-50 text-red-700 border border-red-100"
              }`}>
                {message.text}
              </div>
            )}

            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">Current Password</label>
                <div className="relative">
                  <KeyRound className="absolute left-3 top-2.5 h-5 w-5 text-slate-400" />
                  <input
                    type="password"
                    className="input-base pl-10"
                    placeholder="Enter current password"
                    value={formData.old_password}
                    onChange={(e) => setFormData({ ...formData, old_password: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">New Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-2.5 h-5 w-5 text-slate-400" />
                  <input
                    type="password"
                    className="input-base pl-10"
                    placeholder="Enter new password"
                    value={formData.new_password}
                    onChange={(e) => setFormData({ ...formData, new_password: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">Confirm New Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-2.5 h-5 w-5 text-slate-400" />
                  <input
                    type="password"
                    className="input-base pl-10"
                    placeholder="Confirm new password"
                    value={formData.confirm_password}
                    onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
                    required
                  />
                </div>
              </div>
            </div>

            <div className="pt-4">
              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full py-3 flex justify-center items-center"
              >
                {loading ? <Loader2 className="animate-spin mr-2" size={18} /> : null}
                Change Password
              </button>
            </div>
          </form>
        </div>
      </div>
    </AuthenticatedLayout>
  );
}
