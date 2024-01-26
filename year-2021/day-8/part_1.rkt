#lang racket

(define input_lines
  (file->lines "input-1.txt"))


(set! input_lines
  (map 
    (lambda (line)
      (map
        (lambda (part)
          (string-trim part))
      (string-split line "|")))
    input_lines))

(define number_of_unique_digits 0)
(define unique_lengths '(2 4 3 7))

(for-each
  (lambda (line)
    (for-each
      (lambda (output)
        (if 
          (member (string-length output) unique_lengths)
          (set! number_of_unique_digits (+ number_of_unique_digits 1))
          (set! number_of_unique_digits (+ number_of_unique_digits 0))))
      (string-split (car (cdr line)))))
  input_lines)

(println number_of_unique_digits)
