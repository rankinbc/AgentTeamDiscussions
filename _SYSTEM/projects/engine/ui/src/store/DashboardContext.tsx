import { createContext, useContext, useReducer, type Dispatch, type ReactNode } from 'react';
import { dashboardReducer, type DashboardAction } from './reducer';
import { initialState, type DashboardState } from '../types/state';

interface DashboardContextValue {
  state: DashboardState;
  dispatch: Dispatch<DashboardAction>;
}

const DashboardContext = createContext<DashboardContextValue | null>(null);

export function DashboardProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(dashboardReducer, initialState);
  return (
    <DashboardContext.Provider value={{ state, dispatch }}>
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard(): DashboardContextValue {
  const ctx = useContext(DashboardContext);
  if (!ctx) throw new Error('useDashboard must be used within DashboardProvider');
  return ctx;
}
