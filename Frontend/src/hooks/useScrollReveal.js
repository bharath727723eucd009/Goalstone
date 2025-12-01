import { useEffect, useRef, useState } from 'react';

export const useScrollReveal = (options = {}) => {
  const elementRef = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isVisible) {
          setIsVisible(true);
          observer.unobserve(element);
        }
      },
      {
        threshold: options.threshold || 0.1,
        rootMargin: options.rootMargin || '0px 0px -50px 0px'
      }
    );

    observer.observe(element);

    return () => {
      if (element) observer.unobserve(element);
    };
  }, [isVisible, options.threshold, options.rootMargin]);

  return [elementRef, isVisible];
};

export const ScrollReveal = ({ 
  children, 
  delay = 0, 
  duration = 600,
  direction = 'up',
  type = 'fade',
  className = '',
  ...options 
}) => {
  const [ref, isVisible] = useScrollReveal(options);

  const getTransform = () => {
    if (!isVisible) {
      switch (type) {
        case 'scale':
          return 'scale(0.95)';
        case 'fade':
          switch (direction) {
            case 'left':
              return 'translateX(-24px)';
            case 'right':
              return 'translateX(24px)';
            case 'up':
            default:
              return 'translateY(24px)';
          }
        default:
          return 'translateY(24px)';
      }
    }
    return 'translateY(0) translateX(0) scale(1)';
  };

  return (
    <div
      ref={ref}
      className={`transition-all ease-out ${className}`}
      style={{
        transitionDuration: `${duration}ms`,
        transitionDelay: `${delay}ms`,
        opacity: isVisible ? 1 : 0,
        transform: getTransform()
      }}
    >
      {children}
    </div>
  );
};

export const StaggeredReveal = ({ 
  children, 
  staggerDelay = 100, 
  className = '',
  ...options 
}) => {
  const [ref, isVisible] = useScrollReveal(options);

  return (
    <div ref={ref} className={className}>
      {Array.isArray(children) ? 
        children.map((child, index) => (
          <ScrollReveal key={index} delay={index * staggerDelay}>
            {child}
          </ScrollReveal>
        )) : 
        <ScrollReveal>{children}</ScrollReveal>
      }
    </div>
  );
};