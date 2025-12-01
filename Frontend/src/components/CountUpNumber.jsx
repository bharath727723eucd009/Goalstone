import { useState, useEffect, useRef } from 'react';
import { useScrollReveal } from '../hooks/useScrollReveal';

const CountUpNumber = ({ 
  endValue, 
  durationMs = 900, 
  suffix = '', 
  className = '',
  startOnVisible = true 
}) => {
  const [currentValue, setCurrentValue] = useState(0);
  const [ref, isVisible] = useScrollReveal();
  const animationRef = useRef();
  const startTimeRef = useRef();
  const hasAnimated = useRef(false);

  const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

  const animate = (timestamp) => {
    if (!startTimeRef.current) {
      startTimeRef.current = timestamp;
    }

    const elapsed = timestamp - startTimeRef.current;
    const progress = Math.min(elapsed / durationMs, 1);
    const easedProgress = easeOutCubic(progress);
    
    setCurrentValue(Math.floor(easedProgress * endValue));

    if (progress < 1) {
      animationRef.current = requestAnimationFrame(animate);
    } else {
      setCurrentValue(endValue);
      hasAnimated.current = true;
    }
  };

  useEffect(() => {
    // Reset animation state when endValue changes
    if (hasAnimated.current) {
      hasAnimated.current = false;
      setCurrentValue(0);
    }
  }, [endValue]);

  useEffect(() => {
    const shouldStart = startOnVisible === true ? isVisible : startOnVisible;
    
    if (shouldStart && !hasAnimated.current) {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      startTimeRef.current = null;
      animationRef.current = requestAnimationFrame(animate);
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isVisible, startOnVisible, endValue, durationMs]);

  // Ensure final value is always correct
  useEffect(() => {
    if (hasAnimated.current && currentValue !== endValue) {
      setCurrentValue(endValue);
    }
  }, [endValue, currentValue]);

  return (
    <span ref={startOnVisible === true ? ref : null} className={className}>
      {currentValue}{suffix}
    </span>
  );
};

export default CountUpNumber;