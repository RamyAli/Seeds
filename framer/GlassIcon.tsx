// Glass Icon — animated frosted-glass icon for Framer.
// Paste into a new Framer code file (Assets → Code → New file), then drag it onto the canvas.
import * as React from "react"
import { addPropertyControls, ControlType } from "framer"

const ICONS = [
    "Folder",
    "Toggle",
    "Play",
    "Location",
    "Search",
    "Chat",
    "Download",
    "Windows",
    "Lock",
    "People",
] as const
type IconName = (typeof ICONS)[number]

interface Props {
    icon: IconName
    hue: number
    followSlider: boolean
    animation: "loop" | "hover" | "paused"
    speed: number
    glass: "light" | "dark"
    style?: React.CSSProperties
}

const STAGE_W = 160
const STAGE_H = 140

/**
 * @framerIntrinsicWidth 160
 * @framerIntrinsicHeight 140
 * @framerSupportedLayoutWidth fixed
 * @framerSupportedLayoutHeight fixed
 */
export default function GlassIcon(props: Props) {
    const {
        icon = "Folder",
        hue = 227,
        followSlider = true,
        animation = "loop",
        speed = 1,
        glass = "light",
        style,
    } = props
    const rootRef = React.useRef<HTMLDivElement>(null)
    const [scale, setScale] = React.useState(1)
    const uid = "gi" + React.useId().replace(/[^a-zA-Z0-9]/g, "")

    // Scale the 160 × 140 drawing to whatever size the frame is given
    React.useLayoutEffect(() => {
        const el = rootRef.current
        if (!el || typeof ResizeObserver === "undefined") return
        const update = () => {
            const { width, height } = el.getBoundingClientRect()
            if (width && height) setScale(Math.min(width / STAGE_W, height / STAGE_H))
        }
        update()
        const ro = new ResizeObserver(update)
        ro.observe(el)
        return () => ro.disconnect()
    }, [])

    const rootStyle = {
        ...style,
        "--h": followSlider ? `var(--glass-hue, ${hue})` : String(hue),
        "--speed": String(speed),
    } as React.CSSProperties

    return (
        <div
            ref={rootRef}
            className="gi-root"
            data-mode={animation}
            data-glass={glass}
            style={rootStyle}
            role="img"
            aria-label={icon}
        >
            <style>{CSS}</style>
            <div className={`gi-stage gi-${icon.toLowerCase()}`} style={{ transform: `scale(${scale})` }}>
                {renderIcon(icon, uid)}
            </div>
        </div>
    )
}

addPropertyControls(GlassIcon, {
    icon: { type: ControlType.Enum, title: "Icon", options: [...ICONS], defaultValue: "Folder" },
    hue: {
        type: ControlType.Number,
        title: "Base color",
        min: 0,
        max: 359,
        step: 1,
        unit: "°",
        displayStepper: false,
        defaultValue: 227,
    },
    followSlider: {
        type: ControlType.Boolean,
        title: "Follow slider",
        description: "Use the hue from a Glass Color Slider on the page when there is one.",
        defaultValue: true,
    },
    animation: {
        type: ControlType.Enum,
        title: "Animation",
        options: ["loop", "hover", "paused"],
        optionTitles: ["Loop", "On hover", "Paused"],
        displaySegmentedControl: true,
        defaultValue: "loop",
    },
    speed: { type: ControlType.Number, title: "Speed", min: 0.25, max: 3, step: 0.25, unit: "×", defaultValue: 1 },
    glass: {
        type: ControlType.Enum,
        title: "Glass",
        options: ["light", "dark"],
        optionTitles: ["Light bg", "Dark bg"],
        displaySegmentedControl: true,
        defaultValue: "light",
    },
})

function Grad({ id, dir, reverse }: { id: string; dir: "d" | "v" | "h"; reverse?: boolean }) {
    const xy = { d: [0, 0, 1, 1], v: [0, 0, 0, 1], h: [0, 0, 1, 0] }[dir]
    const stops = reverse ? ["--gc", "--gb", "--ga"] : ["--ga", "--gb", "--gc"]
    return (
        <defs>
            <linearGradient id={id} x1={xy[0]} y1={xy[1]} x2={xy[2]} y2={xy[3]}>
                <stop offset="0" style={{ stopColor: `var(${stops[0]})` }} />
                <stop offset=".52" style={{ stopColor: `var(${stops[1]})` }} />
                <stop offset="1" style={{ stopColor: `var(${stops[2]})` }} />
            </linearGradient>
        </defs>
    )
}

function renderIcon(icon: IconName, uid: string) {
    switch (icon) {
        case "Folder":
            return (
                <>
                    <div className="g paper" />
                    <div className="gl front" />
                </>
            )
        case "Toggle":
            return (
                <>
                    <div className="g orb" />
                    <div className="gl track" />
                    <div className="knob" />
                </>
            )
        case "Play":
            return (
                <>
                    <div className="g back" />
                    <div className="gl front" />
                </>
            )
        case "Location":
            return (
                <>
                    <div className="g land" />
                    <div className="gl pin">
                        <div className="hole" />
                    </div>
                </>
            )
        case "Search":
            return (
                <>
                    <svg className="sv mag" viewBox="0 0 70 70">
                        <Grad id={uid} dir="d" />
                        <circle cx="26" cy="26" r="18" fill="none" stroke={`url(#${uid})`} strokeWidth="7" />
                        <path d="M40 40 L60 60" stroke={`url(#${uid})`} strokeWidth="7" strokeLinecap="round" fill="none" />
                    </svg>
                    <div className="gl bar">
                        <i />
                        <i />
                        <i />
                        <i />
                    </div>
                </>
            )
        case "Chat":
            return (
                <>
                    <div className="g b1" />
                    <div className="gl b2">
                        <div className="typing">
                            <i />
                            <i />
                            <i />
                        </div>
                    </div>
                </>
            )
        case "Download":
            return (
                <>
                    <svg className="sv arrow" viewBox="0 0 36 76">
                        <Grad id={uid} dir="v" reverse />
                        <path d="M18 4 V50" stroke={`url(#${uid})`} strokeWidth="8" strokeLinecap="round" fill="none" />
                        <path
                            d="M5 50 L18 66 L31 50 Z"
                            style={{ fill: "var(--ga)", stroke: "var(--ga)" }}
                            strokeWidth="6"
                            strokeLinejoin="round"
                        />
                    </svg>
                    <div className="gl puff" />
                </>
            )
        case "Windows":
            return (
                <>
                    <div className="g c1" />
                    <div className="gl c2" />
                </>
            )
        case "Lock":
            return (
                <>
                    <svg className="sv shackle" viewBox="0 0 76 66">
                        <Grad id={uid} dir="h" />
                        <path
                            d="M10 64 V36 A28 28 0 0 1 66 36 V64"
                            fill="none"
                            stroke={`url(#${uid})`}
                            strokeWidth="9"
                            strokeLinecap="round"
                        />
                    </svg>
                    <div className="gl body">
                        <div className="key" />
                    </div>
                </>
            )
        case "People":
            return (
                <>
                    <div className="g h2" />
                    <div className="g t2" />
                    <div className="gl h1" />
                    <div className="gl t1" />
                </>
            )
    }
}

const CSS = `
.gi-root {
  position: relative; width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center; overflow: visible;
  --ga: hsl(var(--h) 100% 59%);
  --gb: hsl(var(--h) 100% 72%);
  --gc: hsl(calc(var(--h) + 44) 76% 53%);
  --grad: linear-gradient(140deg, var(--ga) 0%, var(--gb) 52%, var(--gc) 100%);
  --glass: hsl(var(--h) 75% 87% / 0.58);
  --glass-edge: rgba(255, 255, 255, 0.55);
  --knob: #FFFFFF;
  --dot: #FFFFFF;
  --spring: cubic-bezier(.34, 1.56, .64, 1);
  --smooth: cubic-bezier(.65, 0, .35, 1);
}
.gi-root[data-glass="dark"] {
  --glass: hsl(var(--h) 100% 80% / 0.17);
  --glass-edge: rgba(255, 255, 255, 0.16);
  --knob: hsl(var(--h) 100% 97%);
}
.gi-stage { position: relative; width: 160px; height: 140px; flex: none; transform-origin: center; }
.gi-stage * { animation-iteration-count: infinite !important; animation-fill-mode: both !important; }
.gi-root[data-mode="paused"] .gi-stage * { animation-play-state: paused !important; }
.gi-root[data-mode="hover"]:not(:hover) .gi-stage * { animation: none !important; }
@media (prefers-reduced-motion: reduce) { .gi-root[data-mode="loop"] .gi-stage * { animation-play-state: paused !important; } }

.gi-stage .g, .gi-stage .gl, .gi-stage .sv { position: absolute; }
.gi-stage .g { background: var(--grad); }
.gi-stage .sv { overflow: visible; }
.gi-stage .gl {
  background: var(--glass);
  -webkit-backdrop-filter: blur(10px) saturate(150%);
  backdrop-filter: blur(10px) saturate(150%);
  box-shadow: inset 0 0 0 1px var(--glass-edge);
}

.gi-folder .paper { left: 30px; top: 20px; width: 100px; height: 72px; border-radius: 12px; animation: gi-paperLift calc(2.8s / var(--speed)) var(--spring); }
.gi-folder .front { left: 12px; top: 42px; width: 136px; height: 86px; transform-origin: 50% 100%;
  clip-path: path("M16 0 H50 Q57 0 61 6 L66 14 H120 Q136 14 136 30 V70 Q136 86 120 86 H16 Q0 86 0 70 V16 Q0 0 16 0 Z");
  animation: gi-flapOpen calc(2.8s / var(--speed)) var(--smooth); }
@keyframes gi-paperLift { 0%, 15% { transform: translateY(0) } 40%, 65% { transform: translateY(-18px) } 88%, 100% { transform: translateY(0) } }
@keyframes gi-flapOpen { 0%, 15% { transform: perspective(320px) rotateX(0) } 40%, 65% { transform: perspective(320px) rotateX(22deg) } 88%, 100% { transform: perspective(320px) rotateX(0) } }

.gi-toggle .orb { left: 92px; top: 22px; width: 60px; height: 60px; border-radius: 50%; animation: gi-orbPulse calc(3s / var(--speed)) var(--spring); }
.gi-toggle .track { left: 8px; top: 46px; width: 112px; height: 54px; border-radius: 27px; }
.gi-toggle .knob { position: absolute; left: 15px; top: 53px; width: 40px; height: 40px; border-radius: 50%;
  background: var(--knob); box-shadow: 0 2px 8px hsl(var(--h) 100% 59% / .22), inset 0 0 0 2px hsl(var(--h) 100% 72% / .35);
  animation: gi-knobSlide calc(3s / var(--speed)) var(--spring); }
@keyframes gi-knobSlide { 0%, 20% { transform: translateX(0) } 40%, 70% { transform: translateX(58px) } 90%, 100% { transform: translateX(0) } }
@keyframes gi-orbPulse { 0%, 26% { transform: scale(1) } 40%, 70% { transform: translate(-6px, 2px) scale(1.12) } 90%, 100% { transform: scale(1) } }

.gi-play .back { left: 12px; top: 22px; width: 72px; height: 96px;
  clip-path: path("M0 12 Q0 0 11 6 L64 40 Q72 48 64 56 L11 90 Q0 96 0 84 Z");
  animation: gi-nudgeBack calc(2.4s / var(--speed)) var(--spring); }
.gi-play .front { left: 42px; top: 14px; width: 106px; height: 112px;
  clip-path: path("M0 16 Q0 0 15 7 L98 48 Q106 56 98 64 L15 105 Q0 112 0 96 Z");
  animation: gi-nudgeFront calc(2.4s / var(--speed)) var(--spring); }
@keyframes gi-nudgeFront { 0%, 12% { transform: translateX(0) } 34% { transform: translateX(14px) } 52%, 100% { transform: translateX(0) } }
@keyframes gi-nudgeBack { 0%, 20% { transform: translateX(0) } 42% { transform: translateX(14px) } 60%, 100% { transform: translateX(0) } }

.gi-location .land { left: 18px; top: 84px; width: 124px; height: 46px; transform-origin: 50% 100%;
  clip-path: path("M18 0 H106 Q114 0 116 8 L124 38 Q124 46 116 46 H8 Q0 46 0 38 L8 8 Q10 0 18 0 Z");
  animation: gi-landSquash calc(2.8s / var(--speed)) ease-out; }
.gi-location .pin { left: 50px; top: 8px; width: 60px; height: 86px;
  clip-path: path("M30 0 A30 30 0 0 1 60 30 C60 50 42 64 30 86 C18 64 0 50 0 30 A30 30 0 0 1 30 0 Z");
  animation: gi-pinDrop calc(2.8s / var(--speed)) ease-in-out; }
.gi-location .hole { position: absolute; left: 19px; top: 19px; width: 22px; height: 22px; border-radius: 50%; background: rgba(255, 255, 255, .88); }
@keyframes gi-pinDrop {
  0% { transform: translateY(-46px); opacity: 0; animation-timing-function: cubic-bezier(.5, 0, .9, .5); }
  22% { transform: translateY(0); opacity: 1; animation-timing-function: ease-out; }
  30% { transform: translateY(-12px); animation-timing-function: ease-in; }
  38%, 78% { transform: translateY(0); opacity: 1; }
  94%, 100% { transform: translateY(-46px); opacity: 0; }
}
@keyframes gi-landSquash { 0%, 21% { transform: scale(1) } 25% { transform: scale(1.04, .9) } 33%, 37% { transform: scale(1) } 40% { transform: scale(1.02, .96) } 46%, 100% { transform: scale(1) } }

.gi-search .mag { left: 78px; top: 26px; width: 70px; height: 70px; animation: gi-magScan calc(3.2s / var(--speed)) var(--smooth); }
.gi-search .bar { left: 6px; top: 56px; width: 104px; height: 34px; border-radius: 12px; display: flex; align-items: center; gap: 7px; padding-left: 16px; box-sizing: border-box; }
.gi-search .bar i { width: 7px; height: 7px; border-radius: 50%; background: var(--dot); display: block; animation: gi-dotPing calc(3.2s / var(--speed)) ease-out; }
.gi-search .bar i:nth-child(3) { animation-delay: calc(.1s / var(--speed)); }
.gi-search .bar i:nth-child(2) { animation-delay: calc(.2s / var(--speed)); }
.gi-search .bar i:nth-child(1) { animation-delay: calc(.3s / var(--speed)); }
@keyframes gi-magScan { 0%, 10% { transform: translateX(0) } 45%, 58% { transform: translateX(-62px) } 92%, 100% { transform: translateX(0) } }
@keyframes gi-dotPing { 0%, 24% { transform: scale(1) } 32% { transform: scale(1.7) } 42%, 100% { transform: scale(1) } }

.gi-chat .b1 { left: 10px; top: 10px; width: 100px; height: 92px;
  clip-path: path("M14 0 H86 Q100 0 100 14 V60 Q100 74 86 74 H22 L5 91 Q0 94 0 88 V14 Q0 0 14 0 Z");
  animation: gi-floatA calc(3.6s / var(--speed)) ease-in-out; }
.gi-chat .b2 { left: 52px; top: 40px; width: 98px; height: 92px;
  clip-path: path("M14 0 H84 Q98 0 98 14 V88 Q98 94 93 91 L76 74 H14 Q0 74 0 60 V14 Q0 0 14 0 Z");
  animation: gi-floatB calc(3.6s / var(--speed)) ease-in-out; }
.gi-chat .typing { position: absolute; left: 0; top: 0; width: 98px; height: 74px; display: flex; align-items: center; justify-content: center; gap: 6px; }
.gi-chat .typing i { width: 12px; height: 12px; border-radius: 50%; background: var(--dot); display: block; animation: gi-typing calc(1.2s / var(--speed)) ease-in-out; }
.gi-chat .typing i:nth-child(2) { animation-delay: calc(.15s / var(--speed)); }
.gi-chat .typing i:nth-child(3) { animation-delay: calc(.3s / var(--speed)); }
@keyframes gi-typing { 0%, 60%, 100% { transform: translateY(0); opacity: .75 } 30% { transform: translateY(-7px); opacity: 1 } }
@keyframes gi-floatA { 0%, 100% { transform: translate(0, 0) } 50% { transform: translate(-3px, -4px) } }
@keyframes gi-floatB { 0%, 100% { transform: translate(0, 0) } 50% { transform: translate(3px, 3px) } }

.gi-download .arrow { left: 62px; top: 56px; width: 36px; height: 76px; animation: gi-arrowDrop calc(2s / var(--speed)) cubic-bezier(.45, 0, .55, 1); }
.gi-download .puff { left: 10px; top: 8px; width: 142px; height: 90px;
  clip-path: path("M50 90 A45 45 0 1 1 93.8 34.7 A30 30 0 1 1 110 90 Z");
  animation: gi-floatA calc(4s / var(--speed)) ease-in-out; }
@keyframes gi-arrowDrop {
  0% { transform: translateY(-30px); opacity: 0; }
  15% { opacity: 1; }
  42% { transform: translateY(2px); }
  52% { transform: translateY(-3px); }
  60%, 84% { transform: translateY(0); opacity: 1; }
  100% { transform: translateY(14px); opacity: 0; }
}

.gi-windows .c1 { left: 54px; top: 18px; width: 96px; height: 70px; border-radius: 10px; animation: gi-cardBack calc(3.2s / var(--speed)) var(--spring); }
.gi-windows .c2 { left: 10px; top: 52px; width: 96px; height: 70px; border-radius: 10px; animation: gi-cardFront calc(3.2s / var(--speed)) var(--spring); }
@keyframes gi-cardFront { 0%, 15% { transform: translate(0, 0) } 42%, 62% { transform: translate(30px, -22px) } 88%, 100% { transform: translate(0, 0) } }
@keyframes gi-cardBack { 0%, 15% { transform: translate(0, 0) scale(1) } 42%, 62% { transform: translate(6px, 4px) scale(.94) } 88%, 100% { transform: translate(0, 0) scale(1) } }

.gi-lock .shackle { left: 42px; top: 6px; width: 76px; height: 66px; transform-origin: 87% 97%; animation: gi-unlock calc(2.8s / var(--speed)) var(--smooth); }
.gi-lock .body { left: 32px; top: 56px; width: 96px; height: 78px; border-radius: 16px; animation: gi-thud calc(2.8s / var(--speed)) ease-out; }
.gi-lock .key { position: absolute; left: 41px; top: 32px; width: 14px; height: 14px; border-radius: 50%; background: var(--dot); animation: gi-keyGlow calc(2.8s / var(--speed)) ease-out; }
@keyframes gi-unlock {
  0%, 15% { transform: translateY(0) rotate(0) }
  32% { transform: translateY(-16px) rotate(0) }
  42%, 58% { transform: translateY(-16px) rotate(-22deg) }
  68% { transform: translateY(-16px) rotate(0) }
  76% { transform: translateY(2px) rotate(0) }
  82%, 100% { transform: translateY(0) rotate(0) }
}
@keyframes gi-thud { 0%, 75% { transform: translateY(0) } 79% { transform: translateY(3px) } 86%, 100% { transform: translateY(0) } }
@keyframes gi-keyGlow { 0%, 30% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0) } 42%, 58% { transform: scale(1.25); box-shadow: 0 0 0 6px rgba(255, 255, 255, .35) } 70%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0) } }

.gi-people .h2 { left: 78px; top: 10px; width: 50px; height: 50px; border-radius: 50%; animation: gi-peek calc(3s / var(--speed)) var(--spring) calc(.06s / var(--speed)); }
.gi-people .t2 { left: 64px; top: 62px; width: 92px; height: 54px; border-radius: 46px 46px 14px 14px; animation: gi-peek calc(3s / var(--speed)) var(--spring); }
.gi-people .h1 { left: 40px; top: 22px; width: 50px; height: 50px; border-radius: 50%; animation: gi-nod calc(3s / var(--speed)) var(--spring); }
.gi-people .t1 { left: 12px; top: 74px; width: 106px; height: 58px; border-radius: 53px 53px 14px 14px; }
@keyframes gi-peek { 0%, 18% { transform: translateX(0) } 40%, 64% { transform: translateX(12px) } 88%, 100% { transform: translateX(0) } }
@keyframes gi-nod { 0%, 30% { transform: translateY(0) } 40% { transform: translateY(-6px) } 50%, 100% { transform: translateY(0) } }
`
