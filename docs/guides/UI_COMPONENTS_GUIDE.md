# UI Components Guide

## Component Structure

```
src/
├── components/
│   ├── ui/                    # shadcn/ui base components
│   │   ├── button.tsx         # Button component with variants
│   │   ├── card.tsx           # Card container components
│   │   └── badge.tsx          # Badge/label component
│   ├── Header.tsx             # Top navigation bar
│   ├── VideoFeed.tsx          # Main video canvas
│   ├── TrackList.tsx          # Sidebar with tracks
│   ├── TrackCard.tsx          # Individual track card
│   └── MetricsDashboard.tsx   # Bottom metrics panel
├── lib/
│   └── utils.ts               # Utility functions (cn helper)
├── utils/
│   ├── api.ts                 # API client
│   └── canvas.ts              # Canvas drawing utilities
├── hooks/
│   └── useWebSocket.ts        # WebSocket hook
├── types/
│   └── index.ts               # TypeScript types
└── App.tsx                    # Main application

## Using shadcn/ui Components

### Button

```tsx
import { Button } from './components/ui/button';

// Variants
<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// Sizes
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon">Icon</Button>
```

### Card

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>
    Content goes here
  </CardContent>
  <CardFooter>
    Footer content
  </CardFooter>
</Card>
```

### Badge

```tsx
import { Badge } from './components/ui/badge';

<Badge variant="default">Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>
```

## Utility Functions

### cn() - Class Name Merger

```tsx
import { cn } from './lib/utils';

// Merge classes with conditional logic
<div className={cn(
  "base-class",
  isActive && "active-class",
  "another-class"
)} />
```

## Tailwind CSS Classes

### Common Patterns

```tsx
// Spacing
className="p-4 m-2 gap-4 space-y-2"

// Layout
className="flex items-center justify-between"
className="grid grid-cols-2 gap-4"

// Colors
className="bg-background text-foreground"
className="bg-primary text-primary-foreground"
className="bg-card text-card-foreground"

// Borders
className="border border-border rounded-lg"

// Effects
className="hover:bg-accent transition-colors"
className="shadow-lg backdrop-blur"

// Typography
className="text-sm font-medium"
className="font-mono text-xs"
```

### Color System

```css
/* Background colors */
bg-background       /* Main background */
bg-card            /* Card background */
bg-primary         /* Primary green */
bg-secondary       /* Secondary gray */
bg-muted           /* Muted background */
bg-accent          /* Accent background */

/* Text colors */
text-foreground         /* Main text */
text-primary           /* Primary green text */
text-muted-foreground  /* Muted text */
text-destructive       /* Error text */

/* Border colors */
border-border          /* Default border */
border-primary         /* Primary border */
```

## Icons with Lucide React

```tsx
import { Upload, Activity, Lock, Unlock, Eye, Target } from 'lucide-react';

<Upload className="h-4 w-4" />
<Activity className="h-6 w-6 text-primary" />
<Lock className="h-4 w-4" strokeWidth={2} />
```

## Toast Notifications

```tsx
import { toast } from 'sonner';

// Success
toast.success('Operation successful!');

// Error
toast.error('Something went wrong');

// Info
toast.info('Information message');

// Promise
toast.promise(
  fetchData(),
  {
    loading: 'Loading...',
    success: 'Data loaded!',
    error: 'Failed to load',
  }
);
```

## Custom Animations

```tsx
// Pulse glow (defined in tailwind.config.js)
className="animate-pulse-glow"

// Built-in animations
className="animate-pulse"
className="animate-spin"
className="animate-bounce"

// Transitions
className="transition-all duration-200"
className="transition-colors"
```

## Responsive Design

```tsx
// Mobile first approach
className="text-sm md:text-base lg:text-lg"
className="hidden md:flex"
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4"
```

## Adding New Components

To add more shadcn/ui components:

1. Visit https://ui.shadcn.com/docs/components
2. Copy the component code
3. Create file in `src/components/ui/`
4. Import and use in your components

Example components you might want to add:
- Dialog (modals)
- Dropdown Menu
- Tabs
- Tooltip
- Progress
- Slider
- Switch
- Input
- Select

## Best Practices

1. **Use the cn() utility** for conditional classes
2. **Keep components small** and focused
3. **Use TypeScript** for type safety
4. **Follow naming conventions** (PascalCase for components)
5. **Use semantic HTML** (button, nav, main, etc.)
6. **Maintain accessibility** (aria labels, keyboard navigation)
7. **Optimize performance** (memo, useCallback, useMemo)

## Customization

### Changing Colors

Edit `tailwind.config.js`:

```js
colors: {
  primary: {
    DEFAULT: "hsl(142 76% 45%)", // Change this
    foreground: "hsl(222 47% 5%)",
  },
}
```

### Changing Fonts

Edit `tailwind.config.js`:

```js
fontFamily: {
  sans: ['Your Font', 'system-ui', 'sans-serif'],
  mono: ['Your Mono Font', 'monospace'],
}
```

Then import fonts in `index.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Your+Font&display=swap" rel="stylesheet">
```

## Troubleshooting

### Styles not applying
- Check if Tailwind is processing the file (add to `content` in config)
- Clear cache: `npm run build`
- Check for typos in class names

### Components not rendering
- Check imports
- Verify TypeScript types
- Check browser console for errors

### Performance issues
- Use React DevTools Profiler
- Memoize expensive computations
- Lazy load components if needed

Enjoy building with your beautiful component library! 🎨
