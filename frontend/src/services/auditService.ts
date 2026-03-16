import api from "@/services/api";
import { PaginatedResponse } from "@/types/pagination";

export interface AuditLog {
  id: string;
  user_id: string | null;
  username: string | null;
  action: string;
  target_type: string | null;
  target_id: string | null;
  details: any;
  ip_address: string | null;
  created_at: string;
}

export const auditService = {
  getLogs: async (page = 1, limit = 8) => {
    const skip = (page - 1) * limit;
    const response = await api.get<PaginatedResponse<AuditLog>>("/audit-logs/", { params: { skip, limit } });
    return response.data;
  },

  exportLogsPDF: async () => {
    const response = await api.get("/audit-logs/export/pdf", {
      responseType: 'blob'
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'audit_logs_export.pdf');
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
};
