import add from './assets/add-square.svg';
import FeatureFlagItem from "./components/FeatureFlagItem/FeatureFlagItem";
import Header from "./components/Header/Header";
import useListFeatureFlags from "./hooks/useListFeatureFlags";

export default function App() {

  const featureFlags = useListFeatureFlags();

  return (
    <div className="min-h-dvh flex flex-col items-center">
      <Header />
      <main className="w-1/2 mt-12 ">
        <div className='flex justify-between'>
          <h1 className="m-2 text-3xl font-bold text-blue-950">My Feature Flags</h1>
          <img src={add} alt="add feature flag" className='cursor-pointer' />
        </div>
        <hr className="border-gray-200" />
        <ul className=" flex flex-col gap-5 mt-5">
          {featureFlags.map(flag =>
            <FeatureFlagItem key={flag.id} name={flag.name} description={flag.description} value={flag.value} />
          )}
        </ul>
      </main>
    </div>
  )
}
