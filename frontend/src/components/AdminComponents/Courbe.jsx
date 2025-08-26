import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceArea, ResponsiveContainer } from "recharts";

const Courbe = () => {
  const data = [
    { jour: 1, ventes: 120 },
    { jour: 2, ventes: 200 },
    { jour: 3, ventes: 150 },
    { jour: 4, ventes: 300 },
    { jour: 5, ventes: 250 },
    { jour: 6, ventes: 180 },
    { jour: 7, ventes: 220 },
    { jour: 8, ventes: 120 },
    { jour: 9, ventes: 200 },
    { jour: 10, ventes: 150 },
    { jour: 11, ventes: 300 },
    { jour: 12, ventes: 250 },
    { jour: 13, ventes: 180 },
    { jour: 14, ventes: 220 },
    { jour: 15, ventes: 220 },
  ];

  // Trouver la valeur maximale pour ajuster dynamiquement l'échelle Y
  const maxVentes = Math.max(...data.map(item => item.ventes));

  return (
    <div style={{ 
      direction: "rtl", 
      textAlign: "center",
      padding: "20px",
      borderRadius: "12px",
      width: "100%",
      maxWidth: "1000px",
      margin: "0 auto",
      marginBottom: "30px"
    }}>
      <h2 style={{ color: "#374151", marginBottom: "10px" }}>
        تطور المبيعات خلال 15 يوم
      </h2>

      <div style={{ width: '100%', height: '350px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data}
            margin={{ top: 20, right: 50, left: 70, bottom: 50 }}
          >
            {/* ✅ Zone colorée à l'intérieur du graphique */}
            <ReferenceArea
              x1={1} x2={15}   // couvre tout l'axe X
              y1={0} y2={maxVentes * 1.1} // ajusté dynamiquement
              fill="#FAF3DD"
              fillOpacity={1}
            />

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="jour"
              tick={{ fill: "#101011ff" }}
              tickMargin={10}
              label={{ 
                value:"الايام", 
                position: "insideBottomRight",
                dy: 25, 
                fill: "#111827",
                fontSize: "14px"
              }}
            />

            <YAxis
              domain={[0, maxVentes * 1.1]} // Ajustement dynamique avec marge
              tick={{ fill: "#101011ff" }}
              tickMargin={15}
              tickLine={false}
              label={{ 
                value: "إجمالي المبيعات", 
                angle: -90, 
                position: "insideTopLeft", 
                dx: -10,
                dy: 20,
                fill: "#111827",
                fontSize: "14px"
              }}
            />

            <Tooltip
              formatter={(value) => [`${value} مبيعات`, "المبيعات"]}
              labelFormatter={(label) => `اليوم ${label}`}
              contentStyle={{ 
                borderRadius: "8px",
                textAlign: "right",
                direction: "rtl"
              }}
            />

            <Line 
              type="monotone" 
              dataKey="ventes" 
              stroke="#E5B62B" 
              strokeWidth={2} 
              
              
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Courbe;