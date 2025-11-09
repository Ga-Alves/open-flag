import { useState, type ReactNode } from "react"

type ModalProps = {
  children: ReactNode,
  trigger: ReactNode,
}

export default function Modal(props: ModalProps) {

  const { children, trigger } = props;
  const [open, setOpen] = useState(false)
  return (
    <>
      <span onClick={() => setOpen(true)}>
        {trigger}
      </span>
      {
        open &&
        <div className="w-dvw h-dvh bg-[rgba(0,0,0,0.5)] fixed top-0 left-0 z-10 flex items-center justify-center">
          <div className="w-96 h-28 bg-white rounded-lg">
            {children}
            <button className="bg-red-500 rounded-sm cursor-pointer" onClick={() => setOpen(false)}>Close</button>
          </div>
        </div>
      }
    </>
  )
}