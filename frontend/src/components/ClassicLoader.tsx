import type { ComponentProps } from 'react'
import './ClassicLoader.css'

type ClassicLoaderProps = Omit<ComponentProps<'span'>, 'children'>

function ClassicLoader({ className = '', ...props }: ClassicLoaderProps) {
  const loaderClassName = ['classic-loader', className].filter(Boolean).join(' ')

  return (
    <span role="status" className={loaderClassName} {...props}>
      <span className="classic-loader-spokes" aria-hidden="true">
        {Array.from({ length: 12 }, (_, index) => (
          <span
            key={index}
            style={{
              transform: `rotate(${index * 30}deg) translate(146%)`,
              animationDelay: `calc(var(--classic-loader-duration, 1.2s) / 12 * ${index - 12})`,
            }}
          />
        ))}
      </span>
      <span className="screen-reader-only">Loading</span>
    </span>
  )
}

export default ClassicLoader
