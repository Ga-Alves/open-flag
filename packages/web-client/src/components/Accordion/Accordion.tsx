import { useState } from 'react';

export default function Accordion(props: React.PropsWithChildren<{ title: string }>) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="bg-white w-full p-4 rounded-lg shadow-sm mb-4 text-black">
      <div 
        className="flex justify-between items-center cursor-pointer"
        onClick={() => setIsOpen(!isOpen)}
      >
        <h3 className="text-lg font-medium">{props.title}</h3>
        <svg
          className={`w-5 h-5 transition-transform ${isOpen ? 'transform rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>
      
      <div className={`overflow-hidden transition-all duration-300 ${isOpen ? 'mt-4' : 'max-h-0'}`}>
        {props.children}
      </div>
    </div>
  );
}