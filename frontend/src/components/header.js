import "../css/header.css";
import logo from "../assets/logo.png";
export default function Header() {
  return (
    <header className="">
      <div className="wrap-header">
        <div className="container h-full px-7">
          <div className="bg-header flex justify-between items-center w-full h-full">
            {/* Logo */}
            <div className="flex">
              <a href="#">
                <img src={logo} alt="Logo" className="logo" />
              </a>
            </div>
            {/* Menu */}
            <div className="warp-menu h-full px-5-xl px-0-sm ">
              <nav className="menu flex justify-center items-center h-full">
                <ul className="main-menu flex flex-wrap justify-center items-center">
                  <li className="trans-0-4">
                    <a href="#">Home</a>
                  </li>
                  <li className="trans-0-4">
                    <a href="#">About</a>
                  </li>
                  <li className="trans-0-4">
                    <a href="#">Menu</a>
                  </li>
                  <li className="trans-0-4">
                    <a href="#">Reservation</a>
                  </li>
                  <li className="trans-0-4">
                    <a href="#">Contact</a>
                  </li>
                </ul>
              </nav>
            </div>
            {/* Sidebar button */}
            <div className="side-button">
              <button className="btn-show-sidebar trans-0-4"></button>
            </div>
          </div>
        </div>
      </div>    
    </header>
  );
}
