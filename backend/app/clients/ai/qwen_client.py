"""Qwen API client for AI-powered analysis."""

import base64
from typing import Any, Dict, List, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.core.exceptions import AIServiceError

settings = get_settings()


class QwenClient:
    """Client for Alibaba Cloud Qwen API (DashScope compatible mode)."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or settings.QWEN_API_KEY
        self.base_url = base_url or settings.QWEN_BASE_URL
        self.client = httpx.AsyncClient(timeout=120.0)

        if not self.api_key:
            raise AIServiceError("QWEN_API_KEY is not configured")

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        reraise=True
    )
    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: str = "qwen-max",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[str] = None,
    ) -> str:
        """Generate text completion using chat API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (qwen-max, qwen-plus, etc.)
            temperature: Sampling temperature (0.0 - 2.0)
            max_tokens: Maximum tokens in response
            response_format: Optional format ("json" for JSON output)
            
        Returns:
            Generated text content
            
        Raises:
            AIServiceError: If API call fails
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format == "json":
            payload["response_format"] = {"type": "json_object"}

        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=self._get_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            if "choices" not in data or not data["choices"]:
                raise AIServiceError("Empty response from Qwen API")

            return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            error_msg = f"Qwen API error: {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_msg += f" - {error_data.get('error', {}).get('message', '')}"
            except Exception:
                pass
            raise AIServiceError(error_msg)
        except Exception as e:
            raise AIServiceError(f"Qwen API call failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        reraise=True
    )
    async def vision_completion(
        self,
        image_url: str,
        prompt: str,
        model: str = "qwen-vl-max",
        temperature: float = 0.7,
    ) -> str:
        """Analyze an image using vision model.
        
        Args:
            image_url: URL or base64 data URL of the image
            prompt: Text prompt for analysis
            model: Vision model name
            temperature: Sampling temperature
            
        Returns:
            Analysis result text
        """
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": prompt}
                ]
            }
        ]

        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=self._get_headers(),
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                },
            )
            response.raise_for_status()
            data = response.json()

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            raise AIServiceError(f"Vision API call failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        reraise=True
    )
    async def embedding(
        self,
        text: str,
        model: str = "text-embedding-v3",
    ) -> List[float]:
        """Generate text embedding vector.
        
        Args:
            text: Text to embed
            model: Embedding model name
            
        Returns:
            Embedding vector as list of floats
        """
        try:
            response = await self.client.post(
                f"{self.base_url}/embeddings",
                headers=self._get_headers(),
                json={
                    "model": model,
                    "input": text,
                },
            )
            response.raise_for_status()
            data = response.json()

            return data["data"][0]["embedding"]

        except Exception as e:
            raise AIServiceError(f"Embedding API call failed: {str(e)}")

    @staticmethod
    def image_to_data_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
        """Convert image bytes to data URL.
        
        Args:
            image_bytes: Raw image bytes
            mime_type: MIME type of the image
            
        Returns:
            Data URL string
        """
        base64_data = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"
