import deleteIcon from '../../../assets/delete.svg';
import edit from '../../../assets/edit.svg';
import toggleOff from '../../../assets/toggle-off.svg';
import toggleOn from '../../../assets/toggle-on.svg';

type FeatureFlagItemProps = {
    id: number,
    name: string,
    description: string,
    status: boolean,
    deleteFlag: (id: number) => void
    toogleFlag: (id: number, currentStatus: boolean) => void
}
export default function FeatureFlagItem(props: FeatureFlagItemProps) {
    const { description, name, status, deleteFlag, id, toogleFlag } = props
    return (
        <li className="flex">
            <div className="w-1/2">
                <h2 className="text-lg font-bold text-blue-950">{name}</h2>
                <p>{description}</p>
            </div>
            <div className="flex items-center justify-evenly  w-1/2">
                <img src={status ? toggleOn : toggleOff}
                    alt="featureOff"
                    className='cursor-pointer'
                    onClick={() => toogleFlag(id, status)} />
                <img src={edit} alt="edit" className='cursor-pointer' />
                <img src={deleteIcon} alt="delete" className='cursor-pointer' onClick={() => deleteFlag(id)} />
            </div>
        </li>
    )
}