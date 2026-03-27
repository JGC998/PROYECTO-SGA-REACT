import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Topbar from './Topbar'

export default function AppLayout() {
    return (
        <div className="app-layout">
            <Sidebar />
            <div className="main-content fade-in">
                <Topbar />
                <div className="page-container">
                    <Outlet />
                </div>
            </div>
        </div>
    )
}
