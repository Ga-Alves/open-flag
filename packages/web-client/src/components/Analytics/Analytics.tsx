import { useState } from "react";
import Chip from "@mui/material/Chip";
import { LineChart } from "@mui/x-charts/LineChart";

type AnalyticsProps = {
    usageTimeStamps: number[]
}

type ChartData = {
    xAxisData: string[];
    seriesData: number[];
}

type HourlyData = {
    xAxisData: string[];
    seriesData: number[];
}

export function Analytics(props: AnalyticsProps) {
    const { usageTimeStamps } = props;
    const [selectedDate, setSelectedDate] = useState<string | null>(null);

    const { xAxisData, seriesData } = generateChartData(usageTimeStamps);
    const hourlyData = selectedDate ? generateHourlyData(usageTimeStamps, selectedDate) : null;

    const handleDateSelect = (date: string) => {
        setSelectedDate(date === selectedDate ? null : date);
    };

    const handleShowAllHistory = () => {
        setSelectedDate(null);
    };

    return (
        <div className="mt-4 text-black">
            <div className="flex gap-1 flex-wrap mb-4">
                <Chip
                    label='All History'
                    color={!selectedDate ? 'primary' : 'default'}
                    onClick={handleShowAllHistory}
                />
                {xAxisData.map((item) => (
                    <Chip
                        key={item}
                        label={item}
                        color={selectedDate === item ? 'primary' : 'default'}
                        onClick={() => handleDateSelect(item)}
                    />
                ))}
            </div>

            {selectedDate && (
                <div className="mb-4">
                    <h3 className="text-lg font-semibold mb-2">
                        Comportamento no dia {selectedDate}
                    </h3>
                </div>
            )}

            <LineChart
                series={[
                    {
                        data: hourlyData ? hourlyData.seriesData : seriesData,
                        area: true,
                        label: hourlyData ? 'Uso por hora' : 'Uso por dia'
                    },
                ]}
                xAxis={[{
                    data: hourlyData ? hourlyData.xAxisData : xAxisData,
                    scaleType: 'point',
                    label: hourlyData ? 'Horas do dia' : 'Dias'
                }]}
                yAxis={[{
                    label: hourlyData ? 'Quantidade de usos por hora' : 'Quantidade de usos por dia'
                }]}
                height={300}
            />
        </div>
    );
}

function generateChartData(usageTimeStamps: number[]): ChartData {
    const dailyCount: { [key: string]: number } = {};
    
    usageTimeStamps.forEach(timestamp => {
        const date = new Date(timestamp * 1000);
        const dayKey = date.toLocaleDateString('pt-BR');

        dailyCount[dayKey] = (dailyCount[dayKey] || 0) + 1;
    });

    const sortedDates = Object.keys(dailyCount).sort((a, b) => {
        const dateA = new Date(a.split('/').reverse().join('-'));
        const dateB = new Date(b.split('/').reverse().join('-'));
        return dateA.getTime() - dateB.getTime();
    });

    const xAxisData = sortedDates;
    const seriesData = sortedDates.map(date => dailyCount[date]);

    return { xAxisData, seriesData };
}

function generateHourlyData(usageTimeStamps: number[], selectedDate: string): HourlyData {
    const hourlyCount: { [key: string]: number } = {};

    for (let hour = 0; hour < 24; hour++) {
        const hourKey = `${hour.toString().padStart(2, '0')}:00`;
        hourlyCount[hourKey] = 0;
    }

    usageTimeStamps.forEach(timestamp => {
        const date = new Date(timestamp * 1000);
        const dateKey = date.toLocaleDateString('pt-BR');

        if (dateKey === selectedDate) {
            const hour = date.getHours();
            const hourKey = `${hour.toString().padStart(2, '0')}:00`;
            hourlyCount[hourKey]++;
        }
    });

    const xAxisData = Object.keys(hourlyCount);
    const seriesData = Object.values(hourlyCount);

    return { xAxisData, seriesData };
}