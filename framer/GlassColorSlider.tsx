// Glass Color Slider — a live base-color slider for Framer sites.
// Every Glass Icon on the page with "Follow slider" on recolors as visitors drag it.
import * as React from "react"
import { addPropertyControls, ControlType } from "framer"

interface Props {
    hue: number
    label: string
    showValue: boolean
    textColor: string
    font: React.CSSProperties
    style?: React.CSSProperties
}

/**
 * @framerIntrinsicWidth 280
 * @framerIntrinsicHeight 40
 * @framerSupportedLayoutWidth any
 * @framerSupportedLayoutHeight auto
 */
export default function GlassColorSlider(props: Props) {
    const { hue = 227, label = "Base color", showValue = true, textColor = "#1A1D33", font, style } = props
    const [value, setValue] = React.useState(hue)
    const id = "gcs" + React.useId().replace(/[^a-zA-Z0-9]/g, "")

    React.useEffect(() => setValue(hue), [hue])

    // Publish the hue on <html> so every Glass Icon on the page inherits it
    React.useEffect(() => {
        document.documentElement.style.setProperty("--glass-hue", String(value))
    }, [value])

    return (
        <div style={{ ...style, display: "flex", alignItems: "center", gap: 12, color: textColor, ...font }}>
            <style>{`
#${id} { -webkit-appearance: none; appearance: none; flex: 1; min-width: 80px; height: 12px; border-radius: 999px; margin: 0; cursor: pointer;
  background: linear-gradient(90deg, hsl(0 100% 62%), hsl(60 100% 55%), hsl(120 85% 50%), hsl(180 100% 45%), hsl(240 100% 62%), hsl(300 100% 60%), hsl(360 100% 62%)); }
#${id}::-webkit-slider-thumb { -webkit-appearance: none; width: 22px; height: 22px; border-radius: 50%;
  background: hsl(${value} 100% 59%); border: 3px solid #FFFFFF; box-shadow: 0 1px 4px rgba(0, 0, 0, .3); }
#${id}::-moz-range-thumb { width: 16px; height: 16px; border-radius: 50%;
  background: hsl(${value} 100% 59%); border: 3px solid #FFFFFF; box-shadow: 0 1px 4px rgba(0, 0, 0, .3); }
#${id}:focus-visible { outline: 2px solid hsl(${value} 100% 59%); outline-offset: 4px; }
`}</style>
            {label && <label htmlFor={id}>{label}</label>}
            <input
                id={id}
                type="range"
                min={0}
                max={359}
                step={1}
                value={value}
                onChange={(e) => setValue(Number(e.target.value))}
            />
            {showValue && (
                <span style={{ minWidth: "4ch", textAlign: "right", fontVariantNumeric: "tabular-nums", opacity: 0.7 }}>
                    {value}°
                </span>
            )}
        </div>
    )
}

addPropertyControls(GlassColorSlider, {
    hue: { type: ControlType.Number, title: "Start color", min: 0, max: 359, step: 1, unit: "°", defaultValue: 227 },
    label: { type: ControlType.String, title: "Label", defaultValue: "Base color" },
    showValue: { type: ControlType.Boolean, title: "Show value", defaultValue: true },
    textColor: { type: ControlType.Color, title: "Text", defaultValue: "#1A1D33" },
    font: { type: ControlType.Font, title: "Font", controls: "extended", defaultFontType: "sans-serif" } as any,
})
