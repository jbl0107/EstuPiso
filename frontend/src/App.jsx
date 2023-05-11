import {LoginForm} from './components/LoginForm';
import {Navbar} from './components/Navbar.jsx';
import { RegisterForm } from "./components/RegisterForm";
import { Index } from "./components/Index";
import {Routes, Route, useLocation } from "react-router-dom";
import { Announcements } from './components/Announcements';
import { AnnouncementDetails } from './components/AnnouncementDetails';
import { AuthProvider } from './api/AuthContext';


export function App() {

  const location = useLocation();


  return (

    <>
      <AuthProvider>
      {location.pathname !== '/registerForm' && location.pathname !== '/loginForm' && <Navbar />}

      
      <Routes>

        <Route path='/' element={<Index/>} />
        <Route path="/loginForm" element={<LoginForm />} />
        <Route path="/registerForm" element={<RegisterForm />} />
        <Route path="/announcements" element={<Announcements />} />
        <Route path="/announcements/:id" element={<AnnouncementDetails />} />
        
        

      </Routes>
      </AuthProvider>

    </>
  )

}
