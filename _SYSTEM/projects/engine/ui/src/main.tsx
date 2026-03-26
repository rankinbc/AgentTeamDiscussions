import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import { DashboardProvider } from './store/DashboardContext';
import { Dashboard } from './App';
import SetupPage from './pages/SetupPage';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SetupPage />} />
        <Route path="/session" element={
          <DashboardProvider>
            <Dashboard />
          </DashboardProvider>
        } />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
