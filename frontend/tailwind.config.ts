
import type { Config } from "tailwindcss";

export default {
	darkMode: ["class"],
	content: [
		"./pages/**/*.{ts,tsx}",
		"./components/**/*.{ts,tsx}",
		"./app/**/*.{ts,tsx}",
		"./src/**/*.{ts,tsx}",
	],
	prefix: "",
	theme: {
		container: {
			center: true,
			padding: '2rem',
			screens: {
				'2xl': '1400px'
			}
		},
		extend: {
			colors: {
				border: 'hsl(var(--border))',
				input: 'hsl(var(--input))',
				ring: 'hsl(var(--ring))',
				background: 'hsl(var(--background))',
				foreground: 'hsl(var(--foreground))',
				primary: {
					DEFAULT: 'hsl(var(--primary))',
					foreground: 'hsl(var(--primary-foreground))'
				},
				secondary: {
					DEFAULT: 'hsl(var(--secondary))',
					foreground: 'hsl(var(--secondary-foreground))'
				},
				destructive: {
					DEFAULT: 'hsl(var(--destructive))',
					foreground: 'hsl(var(--destructive-foreground))'
				},
				muted: {
					DEFAULT: 'hsl(var(--muted))',
					foreground: 'hsl(var(--muted-foreground))'
				},
				accent: {
					DEFAULT: 'hsl(var(--accent))',
					foreground: 'hsl(var(--accent-foreground))'
				},
				popover: {
					DEFAULT: 'hsl(var(--popover))',
					foreground: 'hsl(var(--popover-foreground))'
				},
				card: {
					DEFAULT: 'hsl(var(--card))',
					foreground: 'hsl(var(--card-foreground))'
				},
				sidebar: {
					DEFAULT: 'hsl(var(--sidebar-background))',
					foreground: 'hsl(var(--sidebar-foreground))',
					primary: 'hsl(var(--sidebar-primary))',
					'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
					accent: 'hsl(var(--sidebar-accent))',
					'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
					border: 'hsl(var(--sidebar-border))',
					ring: 'hsl(var(--sidebar-ring))'
				},
				// Retro theme colors
				retro: {
					beige: '#f0e9db',
					gray: '#9c9c9c',
					darkgray: '#333333',
					lightgray: '#e0e0e0',
					black: '#121212',
					white: '#fafafa',
					blue: '#0084ff',
					purple: '#7b61ff',
					green: '#00A676', // Updated to Leap brand color
					yellow: '#ffcb3d',
				}
			},
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)'
			},
			keyframes: {
				'accordion-down': {
					from: {
						height: '0'
					},
					to: {
						height: 'var(--radix-accordion-content-height)'
					}
				},
				'accordion-up': {
					from: {
						height: 'var(--radix-accordion-content-height)'
					},
					to: {
						height: '0'
					}
				},
				'scanline': {
					'0%': { transform: 'translateY(0%)' },
					'100%': { transform: 'translateY(100%)' }
				},
				'blink': {
					'0%, 100%': { opacity: '1' },
					'50%': { opacity: '0' }
				},
				'crt-flicker': {
					'0%': { opacity: '0.9' },
					'2%': { opacity: '0.5' },
					'3%': { opacity: '0.9' },
					'8%': { opacity: '0.7' },
					'9%': { opacity: '0.9' },
					'100%': { opacity: '0.9' }
				},
				'old-video': {
					'0%': { transform: 'translateX(0) translateY(0)' },
					'25%': { transform: 'translateX(-1px) translateY(1px)' },
					'50%': { transform: 'translateX(1px) translateY(-1px)' },
					'75%': { transform: 'translateX(-1px) translateY(-1px)' },
					'100%': { transform: 'translateX(0) translateY(0)' }
				},
				'loading-progress': {
					'0%': { width: '0%' },
					'100%': { width: '100%' }
				},
				'boot-up': {
					'0%': { opacity: '0', transform: 'scale(0.96)' },
					'30%': { opacity: '0.3', transform: 'scale(0.97)' }, 
					'60%': { opacity: '0.6', transform: 'scale(0.98)' },
					'80%': { opacity: '0.8', transform: 'scale(0.99)' },
					'100%': { opacity: '1', transform: 'scale(1)' }
				},
				'bounce': {
					'0%, 100%': { transform: 'translateY(0)' },
					'50%': { transform: 'translateY(-10px)' }
				}
			},
			animation: {
				'accordion-down': 'accordion-down 0.2s ease-out',
				'accordion-up': 'accordion-up 0.2s ease-out',
				'scanline': 'scanline 8s linear infinite',
				'blink': 'blink 1s infinite',
				'crt-flicker': 'crt-flicker 8s linear infinite',
				'old-video': 'old-video 0.1s infinite',
				'loading-progress': 'loading-progress 2s ease-out',
				'boot-up': 'boot-up 2.5s ease-out',
				'bounce': 'bounce 2s ease-in-out infinite'
			},
			fontFamily: {
				'pixel': ['"Press Start 2P"', 'cursive'],
				'mono': ['"VT323"', 'monospace'],
				'system': ['"IBM Plex Mono"', 'monospace'],
				'outfit': ['"Outfit"', 'sans-serif']
			},
			boxShadow: {
				'retro-inset': 'inset 2px 2px 0px #000000, inset -2px -2px 0px #ffffff',
				'retro-outset': '2px 2px 0px #000000, -2px -2px 0px #ffffff',
				'retro-window': '3px 3px 0px #000000'
			}
		}
	},
	plugins: [require("tailwindcss-animate")],
} satisfies Config;
