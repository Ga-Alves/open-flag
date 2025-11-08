import deleteIcon from '../../assets/delete.svg';
import edit from '../../assets/edit.svg';
import toggleOff from '../../assets/toggle-off.svg';
import toggleOn from '../../assets/toggle-on.svg';

type FeatureFlagItemProps = {
    name: string,
    description: string,
    value: boolean
}
export default function FeatureFlagItem(props: FeatureFlagItemProps) {
    const { description, name, value } = props
    return (
        <li className="flex">
            <div className="w-1/2">
                <h2 className="text-lg font-bold text-blue-950">{name}</h2>
                <p>{description}</p>
            </div>
            <div className="flex items-center justify-evenly  w-1/2">
                {
                    value ? <img src={toggleOn} alt="featureOn" className='cursor-pointer' /> :
                        <img src={toggleOff} alt="featureOff" className='cursor-pointer' />
                }
                <img src={edit} alt="edit" className='cursor-pointer' />
                <img src={deleteIcon} alt="delete" className='cursor-pointer' />
            </div>
        </li>
    )
}