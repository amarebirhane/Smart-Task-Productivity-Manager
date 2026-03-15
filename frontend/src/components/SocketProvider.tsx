"use client";

import React from 'react';
import { useSocket } from '@/hooks/useSocket';
import { useToasts } from '@/components/Toast';

export const SocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { addToast } = useToasts();

  useSocket((type, payload) => {
    if (type === 'notification') {
      addToast(payload.message, 'info', 'New Notification');
    } else if (type === 'task_update') {
      addToast(`Task "${payload.title}" was updated.`, 'success', 'Task Updated');
    }
  });

  return <>{children}</>;
};
捉
