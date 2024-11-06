import logo from "../../assets/staff-logo.png"
import { NavLink } from "react-router-dom"

export default function Navbar() {
    const navItems = [
        {
            name: "Table",
            icon: "table_restaurant",
            path: "table"
        },
        {
            name: "Menu",
            icon: "menu_book",
            path: "menu"
        },
        {
            name: "Reservation",
            icon: "calendar_month",
            path: "reservation"
        },
        {
            name: "History",
            icon: "history",
            path: "history"
        },
        {
            name: "Order",
            icon: "checklist",
            path: "order-queue"
        },
        {
            name: "Manager",
            icon: "group",
            path: "manager"
        }
    ]


    return(
        <nav className="flex flex-col justify-between h-[100%]">

                <div>
                    <img src={logo} className="mx-auto mt-1" alt="logo" width="90%" height="90%"/>
                    <div className="flex flex-col text-honeydew gap-4 mt-[4vw]">
                        {navItems.map((item, index) => (
                            <NavLink key={index} to={item.path} className="text-center nav-items">
                                <div className="box-border">
                                    <i class="material-symbols-outlined text-[3vw]">{item.icon}</i>
                                    <p className="text-[0.8vw] mt-[-0.7vw] font-medium">{item.name}</p>  
                                </div>         
                            </NavLink>
                        ))}
                    </div>
                </div> 
                <i class="material-symbols-outlined mx-auto text-[3vw] mb-1 text-honeydew bottom-0 cursor-pointer">logout</i>

                
        </nav>
    )
}