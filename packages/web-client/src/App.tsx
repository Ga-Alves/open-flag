import add from './assets/add-square.svg';
import FeatureFlagList from './components/FeatureFlagList/FeatureFlagList';
import Header from "./components/Header/Header";

export default function App() {


  return (
    <div className="min-h-dvh flex flex-col items-center">
      <Header />
      <main className="w-1/2 mt-12 ">
        <div className='flex justify-between'>
          <h1 className="m-2 text-3xl font-bold text-blue-950">My Feature Flags</h1>
          <img src={add} alt="add feature flag" className='cursor-pointer' />
        </div>
        <hr className="border-gray-200" />
        <FeatureFlagList />
      </main>
    </div>
  )
}
