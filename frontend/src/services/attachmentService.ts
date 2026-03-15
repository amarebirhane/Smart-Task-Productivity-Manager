import api from './api';
import { Attachment } from '../types/task';

export const attachmentService = {
  uploadAttachment: async (taskId: string, file: File, onProgress?: (percent: number) => void) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<Attachment>(`/attachments/upload/${taskId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted);
        }
      },
    });
    return response.data;
  },

  getTaskAttachments: async (taskId: string) => {
    const response = await api.get<Attachment[]>(`/attachments/task/${taskId}`);
    return response.data;
  },

  deleteAttachment: async (attachmentId: string) => {
    const response = await api.delete(`/attachments/${attachmentId}`);
    return response.data;
  },
};

export default attachmentService;
