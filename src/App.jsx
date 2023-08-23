import { Route, Routes } from "react-router-dom";
import "./App.css";
import { Navbar } from "./components/Navbar";
import { PrivateRoute, PublicRoute } from './PrivateRoute';
import { About, PredictionHistory, Predict, UserProfile, Login, Register, Logout, UserList} from "./components/pages";

function App() {
  
  return (
    <div className="App">
      <Navbar />
      <Routes>

        <Route path="/login" element={<PublicRoute> <Login /> </PublicRoute>} />
        <Route path="/register"element={<PublicRoute> <Register /> </PublicRoute>} />
        <Route path="/logout" element={<PrivateRoute> <Logout /> </PrivateRoute>} />

        <Route path="/" element={<PrivateRoute> <Predict /> </PrivateRoute>} />
        <Route path="/predict" element={<PrivateRoute> <Predict /> </PrivateRoute>} />
        <Route path="/about" element={<PrivateRoute> <About /> </PrivateRoute>} />
        <Route path="/user/profile" element={<PrivateRoute> <UserProfile /> </PrivateRoute>} />
        <Route path="/predication-history" element={<PrivateRoute> <PredictionHistory /> </PrivateRoute>} />
        <Route path="/admin/users" element={<PrivateRoute> <UserList /> </PrivateRoute>} />
        

      </Routes>
    </div>
  );
}

export default App;
