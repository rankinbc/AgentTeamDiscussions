import { useEffect } from 'react';
import type { Dispatch } from 'react';
import type { DashboardAction } from '../store/reducer';
import type { SSEEvent } from '../types/events';

export function useSSE(dispatch: Dispatch<DashboardAction>) {
  useEffect(() => {
    const es = new EventSource('/events');

    es.onopen = () => {
      dispatch({ type: 'UI_SET_CONNECTION', status: 'live' });
    };

    es.onerror = () => {
      dispatch({ type: 'UI_SET_CONNECTION', status: 'disconnected' });
    };

    es.onmessage = (e) => {
      try {
        const event = JSON.parse(e.data) as SSEEvent;
        dispatch({ type: 'SSE_EVENT', event });
      } catch (ex) {
        console.error('SSE parse error:', ex);
      }
    };

    return () => {
      es.close();
    };
  }, [dispatch]);
}
