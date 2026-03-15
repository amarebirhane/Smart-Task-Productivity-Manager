"use client";

import React, { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { authService } from "@/features/auth/authService";
import AuthenticatedLayout from "@/components/AuthenticatedLayout";
import { getErrorMessage } from "@/utils/errorHandler";
import { useToasts } from "@/components/Toast";
import { User, UserCheck, Mail, Loader2, Save } from "lucide-react";

export default function ProfilePage() {
  const { user, setUser } = useAuth();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
  });
  const [loading, setLoading] = useState(false);
  const { addToast } = useToasts();

  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username || "",
        email: user.email || "",
        first_name: user.first_name || "",
        last_name: user.last_name || "",
      });
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const updatedUser = await authService.updateProfile(formData);
      setUser(updatedUser);
      addToast("Profile updated successfully!", "success");
    } catch (err: any) {
      addToast(getErrorMessage(err, "Failed to update profile."), "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthenticatedLayout>
      <div className="max-w-4xl mx-auto py-8 px-4">
        <div className="flex items-center space-x-4 mb-8">
          <div className="h-16 w-16 bg-primary-100 rounded-full flex items-center justify-center text-primary-600">
            <User size={32} />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">User Profile</h1>
            <p className="text-slate-500">Manage your personal information</p>
          </div>
        </div>

        <div className="card-premium p-6">
          <form onSubmit={handleSubmit} className="space-y-6">

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">Username</label>
                <div className="relative">
                  <UserCheck className="absolute left-3 top-2.5 h-5 w-5 text-slate-400" />
                  <input
                    type="text"
                    className="input-base pl-10"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-2.5 h-5 w-5 text-slate-400" />
                  <input
                    type="email"
                    className="input-base pl-10"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">First Name</label>
                <input
                  type="text"
                  className="input-base"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">Last Name</label>
                <input
                  type="text"
                  className="input-base"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  required
                />
              </div>
            </div>

            <div className="pt-4 flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className="btn-primary flex items-center space-x-2 px-6 py-2"
              >
                {loading ? <Loader2 className="animate-spin" size={18} /> : <Save size={18} />}
                <span>Save Changes</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </AuthenticatedLayout>
  );
}
