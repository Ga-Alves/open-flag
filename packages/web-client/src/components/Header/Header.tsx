import logo from '../../assets/logo.svg'

export default function Header() {
    return (
        <header className="w-full h-20 bg-blue-950 flex items-center pl-3.5">
            <img src={logo} alt="Logo" />
            <h1 className="text-white text-4xl font-bold">Open Flag</h1>
        </header>
    )
}