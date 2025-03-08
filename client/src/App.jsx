import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'

import Login from './pages/Login/Login.jsx'
import Dashboard from './pages/Dashboard/Dashboard.jsx'
import Home from './pages/Home/Home.jsx'
import Membros from './pages/Membros/Membros.jsx'
import Prototipos from './pages/Prototipos/Prototipos.jsx'
import Sensores from "./pages/Sensores/Sensores.jsx"
import Metodologia from './pages/Metodologia/Metodologia.jsx'
import Pilotos from './pages/Pilotos/Pilotos.jsx'
import Circuito from './pages/Circuito/Circuito.jsx'
import Teste from './pages/Testes/Testes.jsx'
import TRPM from './pages/TRPM/TRPM.jsx'
import Logger from './pages/Logger/Logger.jsx'
import Anexos from './pages/Anexos/Anexos.jsx'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
          <Route path='/prototipo' element={<Prototipos/>} />
          <Route path="/inicio" element={<Dashboard />} />
          <Route path='/membros' element={<Membros/>}/>
          <Route path='/sensores' element={<Sensores/>}/>
          <Route path='/metodologia' element={<Metodologia/>}/>
          <Route path='/pilotos' element={<Pilotos/>}/>
          <Route path='/circuito' element={<Circuito/>}/>
          <Route path='/teste' element={<Teste/>}/>
          <Route path='/TRPM' element={<TRPM/>}/>
          <Route path='/logger' element={<Logger/>}/>
          <Route path='/anexos' element={<Anexos/>}/>
        </Route>

      </Routes>
    </Router>
  )
}

export default App